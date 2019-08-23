# LastFM Album Collage Maker
Command line album collage maker for lastFM scrobbles

## Usage
```
collage-cmd.py [-h] -u USERNAME -k KEY [-p {7day,1month,3month,6month,12month,overall}] [-s ROWSxCOLUMNS]

arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        LastFM username
  -k KEY, --key KEY     LastFM api key
  -p {7day,1month,3month,6month,12month,overall}, --period {7day,1month,3month,6month,12month,overall}
                        Scrobbling period
  -s ROWSxCOLUMNS, --size ROWSxCOLUMNS
                        Collage dimensions - format ROWSxCOLUMNS (3x3, 4x5, 2x7, etc)
```
