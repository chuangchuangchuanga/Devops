from fabric.main import *


def _escape_split(sep, argstr):
    """
    Allows for escaping of the separator: e.g. task:arg='foo\, bar'
    It should be noted that the way bash et. al. do command line parsing, those
    single quotes are required.
    """
    escaped_sep = r'\%s' % sep

    if escaped_sep not in argstr:
        return argstr.split(sep)

    before, _, after = argstr.partition(escaped_sep)
    startlist = before.split(sep)  # a regular split is fine here
    unfinished = startlist[-1]
    startlist = startlist[:-1]

    # recurse because there may be more escaped separators
    endlist = _escape_split(sep, after)

    # finish building the escaped value. we use endlist[0] becaue the first
    # part of the string sent in recursion is the rest of the escaped value.
    unfinished += sep + endlist[0]

    return startlist + [unfinished] + endlist[1:]  # put together all the parts


def main(fabfile_locations=None):
    """
    Main command-line execution loop.
    """
    try:
        # Parse command line options
        parser, options, arguments = parse_options()

        # Handle regular args vs -- args
        arguments = parser.largs
        remainder_arguments = parser.rargs

        # Allow setting of arbitrary env keys.
        # This comes *before* the "specific" env_options so that those may
        # override these ones. Specific should override generic, if somebody
        # was silly enough to specify the same key in both places.
        # E.g. "fab --set shell=foo --shell=bar" should have env.shell set to
        # 'bar', not 'foo'.
        for pair in _escape_split(',', options.env_settings):
            pair = _escape_split('=', pair)
            # "--set x" => set env.x to True
            # "--set x=" => set env.x to ""
            key = pair[0]
            value = True
            if len(pair) == 2:
                value = pair[1]
            state.env[key] = value

        # Update env with any overridden option values
        # NOTE: This needs to remain the first thing that occurs
        # post-parsing, since so many things hinge on the values in env.
        for option in env_options:
            state.env[option.dest] = getattr(options, option.dest)

        # Handle --hosts, --roles, --exclude-hosts (comma separated string =>
        # list)
        for key in ['hosts', 'roles', 'exclude_hosts']:
            if key in state.env and isinstance(state.env[key], basestring):
                state.env[key] = state.env[key].split(',')

        # Feed the env.tasks : tasks that are asked to be executed.
        state.env['tasks'] = arguments

        # Handle output control level show/hide
        update_output_levels(show=options.show, hide=options.hide)

        # Handle version number option
        if options.show_version:
            print("Fabric %s" % state.env.version)
            print("Paramiko %s" % ssh.__version__)
            sys.exit(0)

        # Load settings from user settings file, into shared env dict.
        state.env.update(load_settings(state.env.rcfile))

        # Find local fabfile path or abort
        fabfile = find_fabfile(fabfile_locations)
        if not fabfile and not remainder_arguments:
            abort("""Couldn't find any fabfiles!
Remember that -f can be used to specify fabfile path, and use -h for help.""")

        # Store absolute path to fabfile in case anyone needs it
        state.env.real_fabfile = fabfile

        # Load fabfile (which calls its module-level code, including
        # tweaks to env values) and put its commands in the shared commands
        # dict
        default = None
        if fabfile:
            docstring, callables, default = load_fabfile(fabfile)
            state.commands.update(callables)

        # Handle case where we were called bare, i.e. just "fab", and print
        # a help message.
        actions = (options.list_commands, options.shortlist, options.display,
            arguments, remainder_arguments, default)
        if not any(actions):
            parser.print_help()
            sys.exit(1)

        # Abort if no commands found
        if not state.commands and not remainder_arguments:
            abort("Fabfile didn't contain any commands!")

        # Now that we're settled on a fabfile, inform user.
        if state.output.debug:
            if fabfile:
                print("Using fabfile '%s'" % fabfile)
            else:
                print("No fabfile loaded -- remainder command only")

        # Shortlist is now just an alias for the "short" list format;
        # it overrides use of --list-format if somebody were to specify both
        if options.shortlist:
            options.list_format = 'short'
            options.list_commands = True

        # List available commands
        if options.list_commands:
            show_commands(docstring, options.list_format)

        # Handle show (command-specific help) option
        if options.display:
            display_command(options.display)

        # If user didn't specify any commands to run, show help
        if not (arguments or remainder_arguments or default):
            parser.print_help()
            sys.exit(0)  # Or should it exit with error (1)?

        # Parse arguments into commands to run (plus args/kwargs/hosts)
        commands_to_run = parse_arguments(arguments)

        # Parse remainders into a faux "command" to execute
        remainder_command = parse_remainder(remainder_arguments)

        # Figure out if any specified task names are invalid
        unknown_commands = []
        for tup in commands_to_run:
            if crawl(tup[0], state.commands) is None:
                unknown_commands.append(tup[0])

        # Abort if any unknown commands were specified
        if unknown_commands and not state.env.get('skip_unknown_tasks', False):
            warn("Command(s) not found:\n%s" \
                % indent(unknown_commands))
            show_commands(None, options.list_format, 1)

        # Generate remainder command and insert into commands, commands_to_run
        if remainder_command:
            r = '<remainder>'
            state.commands[r] = lambda: api.run(remainder_command)
            commands_to_run.append((r, [], {}, [], [], []))

        # Ditto for a default, if found
        if not commands_to_run and default:
            commands_to_run.append((default.name, [], {}, [], [], []))

        # Initial password prompt, if requested
        if options.initial_password_prompt:
            prompt = "Initial value for env.password: "
            state.env.password = getpass.getpass(prompt)

        # Ditto sudo_password
        if options.initial_sudo_password_prompt:
            prompt = "Initial value for env.sudo_password: "
            state.env.sudo_password = getpass.getpass(prompt)

        if state.output.debug:
            names = ", ".join(x[0] for x in commands_to_run)
            print("Commands to run: %s" % names)

        # At this point all commands must exist, so execute them in order.
        for name, args, kwargs, arg_hosts, arg_roles, arg_exclude_hosts in commands_to_run:
            execute(
                name,
                hosts=arg_hosts,
                roles=arg_roles,
                exclude_hosts=arg_exclude_hosts,
                *args, **kwargs
            )
        # If we got here, no errors occurred, so print a final note.
        if state.output.status:
            print("\nDone.")
    except SystemExit:
        # a number of internal functions might raise this one.
        raise
    except KeyboardInterrupt:
        if state.output.status:
            sys.stderr.write("\nStopped.\n")
        sys.exit(1)
    except:
        sys.excepthook(*sys.exc_info())
        # we might leave stale threads if we don't explicitly exit()
        sys.exit(1)
    finally:
        disconnect_all()
    sys.exit(0)


if __name__ == "__main__":
    main()