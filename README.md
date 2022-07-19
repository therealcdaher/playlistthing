# playlistthing, a thing for playlists  
The goal of this application is to build an automated way to push all of your playlists to all of your devices. I'm sure other stuff exists for this purpose, it's more of an exercise/for fun. It's meant to piggyback off of Syncthing to move the actual files to your actual devices, at least for now, although that's not strictly necessary if you're serving your music off of a central SMB server or something like that. 

---
## Basic spec/description
Continuously-running application (more of a service), meant to run on the server where your media is hosted. The user will provide the following information through a web GUI:  
1. Playlist source folder
2. Playlist source file path, if different from what it is on the media server (for example, if you create your playlists on a desktop machine and access the files via SMB share)
3. Playlist destination top folder
4. Music source folder
5. Music destination folder
6. The path to the music destination folder as it is on the device(s) that the playlists will be converted for
7. The desired time interval for content rescans 

The application will then:  
1. Scan the source playlist folder per the interval set by the user
2. When a playlist is found:
   1. Check if music destination already contain files referenced in playlist
      1. If it does not, copy them over
   2. Hash check destination files against source files
      1. Recopy if it does not match
   3. Check if the converted playlist already exists
      1. If not, convert the original to the structure used by the intended device, and store it in a sub-folder of the playlist destination top folder that will be referenced by that device as the playlist directory
3. Do nothing until it's time for the next check

You should then either use something like Syncthing to sync the desired destination folders over to your device(s), or simply mount them as network shares. The music destination folder can be universal, but each device will need its own playlist folder, otherwise this would need a companion application on the intended device to re-convert the playlist to use the appropriate file structure.  

Backend will be in Python, haven't decided on the frontend yet. 

Haven't even started development yet, but I probably will eventually. Just want to give myself something clear to work towards for now.  