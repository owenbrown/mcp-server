import os
import platform
from textwrap import dedent


def check_veryfi_credentials():
    """Check if Veryfi credentials are properly set and return detailed error message if not."""
    missing_vars = []
    empty_vars = []

    # Check each required variable
    for var_name in ["VERYFI_CLIENT_ID", "VERYFI_USERNAME", "VERYFI_API_KEY"]:
        value = os.getenv(var_name)
        if value is None:
            missing_vars.append(var_name)
        elif value.strip() == "":
            empty_vars.append(var_name)

    if not missing_vars and not empty_vars:
        return None  # All credentials are properly set

    # Build error message parts
    error_parts = []

    # Header
    error_parts.append("## Missing Veryfi Credentials\n")

    # List missing/empty variables
    if missing_vars or empty_vars:
        error_parts.append("The following environment variables are required but not properly set:\n")

        for var in missing_vars:
            error_parts.append(f"• **{var}** - Not found in environment")

        for var in empty_vars:
            error_parts.append(f"• **{var}** - Set but empty")

    # Add debugging help section
    debug_code = "\n".join(
        [
            "import os",
            *[
                f"print('{var}:', os.environ.get('{var}', 'Not set'))"
                for var in ["VERYFI_CLIENT_ID", "VERYFI_USERNAME", "VERYFI_API_KEY"]
            ],
        ]
    )

    error_parts.extend(
        [
            "\n### Debug your current environment\n",
            "You can check your current environment variables by running:\n",
            f"```python\n{debug_code}\n```\n",
        ]
    )

    # Add setup instructions
    error_parts.extend(
        [
            "### How to fix this\n",
            "These values can be found in the Veryfi Hub. Visit https://app.veryfi.com, ",
            "and sign into your account. Next, navigate to https://app.veryfi.com/api/settings/keys/\n",
        ]
    )

    # Option 1: .env file
    env_file_content = dedent(
        """
        VERYFI_CLIENT_ID="your-client-id-here"
        VERYFI_USERNAME="your-username-here"
        VERYFI_API_KEY="your-api-key-here"
    """
    ).strip()

    # Explain environment variable precedence
    env_explanation = dedent(
        """
        #### Understand how env variables are set

        The Veryfi MCP uses dotenv. It will look for a file, .env,
        in the folder containing the MCP server, and in all ancestor folders.
        If your environment variables are set here, they overwrite all other env variables.

        Your AI agent's setting will overwrite env variables set in your execution environment.
        For example, Claude variables are set in ~/.claude.json.
        Since you'll want to use environment variables or .env files to call Veryfi's API from your
        code, for most use cases you should not set the environment variables here.

        You can set your environment variables using other methods. For example, on a mac
        you can set them by editing your .zprofile or .bashrc file.
        IMPORTANT: If you reset variables this way, make sure to quit and restart VSCode / Cursor,
        and to create a new session if you're using a CLI tool like Claude Code.
        This means that you should not set the environment variables in your agent settings.
        """
    ).strip()

    error_parts.extend(
        [
            "\n" + env_explanation,
            f"```\n{env_file_content}\n```\n",
        ]
    )

    return "\n".join(error_parts)
