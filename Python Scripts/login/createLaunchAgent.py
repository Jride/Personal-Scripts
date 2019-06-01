import os
import sys

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser

### --- MAIN --- ###

parser = itv_argparser.parser(
os.path.dirname(__file__),
'Creates the launch agent plist and loads it with launchctl'
)
args = parser.parse_args(sys.argv[1:])

home_dir = os.path.expanduser('~') + "/"
launch_agent_location = home_dir + "Library/LaunchAgents/"
file_name = "com.loginHook.plist"

login_hook_script = home_dir + "Documents/.packageUpdates/loginHook.sh"

file = open(launch_agent_location + file_name, "w+")
file.write('''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>EnvironmentVariables</key>
    <dict>
      <key>PATH</key>
      <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:</string>
    </dict>
    <key>Label</key>
    <string>com.loginHook</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>%s</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>09</integer>
        <key>Minute</key>
        <integer>00</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/loginHook.stdout</string>
    <key>StandardErrorPath</key>
    <string>/tmp/loginHook.stderr</string>
  </dict>
</plist>
''' % (login_hook_script))
file.close()

itv_shell.run("launchctl unload " + launch_agent_location + file_name)
itv_shell.run("launchctl load " + launch_agent_location + file_name)
