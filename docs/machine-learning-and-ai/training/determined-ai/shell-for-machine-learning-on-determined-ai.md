---
description: Use a shell for freeform commands with Determined AI
---

# Shell for Machine Learning on Determined AI

Determined AI supports the use of commands and shells in order to engage with Determined clusters and cluster GPUs without needing to use the trial APIs or for running existing code in batch mode.

On Determined AI, shells start SSH servers, which in turn provide access to the cluster and its resources in the form of interactive SSH sessions.

{% hint style="info" %}
**Additional Resources**

For more information, refer to the official Determined AI documentation regarding [the CLI tool `det`](https://docs.determined.ai/latest/interfaces/commands-and-shells.html#command-line-interface-cli-reference) and [shells on Determined AI](https://docs.determined.ai/latest/interfaces/commands-and-shells.html#shells).
{% endhint %}

## Setup

Before continuing with the rest of this guide, first [install and configure the Determined AI application via the Cloud UI](../../../compass/determined-ai/gpt-neox.md#install-the-determined-application) into your namespace.

Next, create a Python virtual environment using a tool such as `venv` or `virtualenv` on your local environment. Then, install the Determined AI CLI tool using `pip`:

```bash
$ pip install determined==0.19.8
```

## Create a shell

Using the Determined CLI tool (`det`), create a shell by invoking:

```bash
$ det shell start
```

## Connect to Visual Studio Code Remote

It is possible to integrate Determined shells with Visual Studio. To do so, first ensure the extension [Visual Studio Code Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) is installed in Visual Studio.

Then, either acquire the SSH connection command by starting a new shell with the `--show-ssh-command` option:

```bash
$ det shell start --show-ssh-command
```

Or, get the SSH command for an existing shell by using `show_ssh_command`:

```bash
$ det shell show_ssh_command <SHELL UUID>
```

Copy the output SSH command.

From Visual Studio, navigate to the **Command Palette**. Select **Remote-SSH: Add new SSH Host...**.

When prompted, paste the copied SSH command into the dialogue box. The final prompt will be to select a configuration file; the default file should work for most users.

The remote host will now be available in [the Visual Studio Code **Remote Explorer**](https://code.visualstudio.com/docs/remote/ssh).

{% hint style="info" %}
**Note**

For more information regarding IDE integration with Determined AI, refer to [the Determined AI documentation's article on IDE integration](https://docs.determined.ai/latest/interfaces/ide-integration.html) or [the official Visual Studio Code Remote SSH extension](https://code.visualstudio.com/docs/remote/ssh) documentation.
{% endhint %}

## Commands

Determined AI CLI commands start with `det command`, abbreviated as `det cmd`. The main sub-command is `det cmd run`, which runs a command in the cluster and streams its output.

For example, the following CLI command uses `nvidia-smi` to display information about the GPUs available to tasks in the container:

```bash
$ det cmd run nvidia-smi
```

More complex commands, including shell constructs, can also be run. These must be quoted to prevent interpretation by the local shell:

```bash
$ det cmd run 'for x in a b c; do echo $x; done'
```

{% hint style="warning" %}
**Important**

The `det cmd run` command streams its output until it exits, but the command will continue executing - and occupying cluster resources - even if the CLI is interrupted (`Ctrl-C`) or killed.
{% endhint %}

To **stop** the command, or to view additional output, first acquire the command UUID. Command UUIDs are output with the oriignal output of the first `det cmd run`, or can be found by running `det cmd list`. Once you have the command's UUID, you may perform additional operations, such as:

| Command                  | Operation                                                   |
| ------------------------ | ----------------------------------------------------------- |
| `det cmd logs <UUID>`    | View a snapshot of logs                                     |
| `det cmd logs -f <UUID>` | View the current logs, and continue streaming future output |
| `det cmd kill <UUID>`    | Stop the command                                            |

{% hint style="info" %}
**Additional Resources**

Refer to [the Determined AI documentation on shell commands](https://docs.determined.ai/latest/interfaces/commands-and-shells.html#commands) for more information on `det` shell commands.
{% endhint %}
