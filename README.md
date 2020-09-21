# Hearthstone Battlegrounds Skip

### A useful tool to skip battles in Hearthstone Battlegrounds !
This tool uses an exploit in Hearthstone Battlegrounds to skip battles. It enables you to disconnect and reconnect quickly from the game, so that when you reconnect, you will be in the recruit phase.

# How to use ?
Work only with **Windows**.
1. Download HSBGSkip.exe
2. If necessary, allow the program in your firewall.
3. Right-click on the .exe, go into properties -> Compatibility -> Check "Run as Admin" -> Apply
3. Launch it as admin, the first time you launch it, select Hearthstone.exe in your Hearthstone game folder (default: `C:\program files (x86)\Hearthstone`)
4. When you want to skip the battle, press skip just before the end of the recruit phase (i.e. when you see 2 or 3 sec left). 
You can also skip when you are already in combat.

If you are not confident by authorizing HSBGSkip.exe, you can build it yourself. The code is in the branch 'development'. Git clone the development branch and either launch skip.py with python, or you can compile it using pyinstaller with this command :  
`pyinstaller --clean --onefile --noconsole --icon="data_files/next.ico" --add-data="data_files/next.ico;data_files" skip.py`

# How it works ?
When you launch it, it creates an outbound rule in the windows firewall to block hearthstone.exe to send data to the server.
When you press skip, it enables the rule for 4 seconds and disable it afterwards. Thus, you lost the connexion with the server in the game, and a first popup informs you that you have been disconnected, and after the delay, a second pop up informs you that you have been reconnected to the game.

You can modify the delay in the config.json file stored in `%APPDATA%/HearthstoneBattlegroundsSkip/` 

The app was written in Python and the executable was created with PyInstaller.

# FAQ
