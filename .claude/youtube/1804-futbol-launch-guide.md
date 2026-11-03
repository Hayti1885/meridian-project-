# 1804 Futbol: Launch Guide

Your plan to launch the 1804 Futbol channel around Haiti vs USA in the CONCACAF Nations League
quarterfinal. Work top to bottom and tick each box.

## Key dates

| Date | Event |
|---|---|
| Tue Nov 3 to Tue Nov 10 | Set up accounts, record clips |
| Thu Nov 12 | Post the preview Short |
| Sat Nov 14, 4:30 pm ET | Leg 1, Nu Stadium, Miami |
| Sat Nov 14, same night | Post the Leg 1 reaction Short |
| Tue Nov 17 | Leg 2, TQL Stadium, Cincinnati. Post the Leg 2 reaction that night |
| March 2027 | Nations League final four in Los Angeles, if Haiti advances |

## Phase 1: Accounts (by Tue Nov 10)

- [ ] Create a new Gmail for the channel, such as one with 1804futbol in the address
- [ ] Turn on 2-step verification on that Gmail
- [ ] YouTube: create channel "1804 Futbol", handle @1804Futbol (backup: @1804FutbolHT)
- [ ] TikTok: claim username 1804Futbol
- [ ] Instagram: claim username 1804futbol
- [ ] Use the same handle on all 3. If one is taken, switch all 3 to the backup.
- [ ] Paste this into the YouTube About section:

```
Haiti football, from the fans. Previews, reactions and the road to the World Cup.
1804: the year Haiti became free. Ayiti, nou la!
Fan channel, not affiliated with the FHF.
```

- [ ] Send Claude the 3 handles you got

## Phase 2: Produce the preview Short (by Wed Nov 11)

Approved package:

```
TITLE:  Can Haiti Beat the US? It Starts Nov 14
COVER:  ROAD TO LA
HOOK:   You have never seen Haiti play the US in the Nations League,
        but nobody should miss what happens November 14 in Miami.
```

- [ ] Fact check: confirm on ussoccer.com that "9-6-9" means 9 US wins, 6 Haiti wins, 9 draws.
      If you cannot confirm it, say "the all-time record is 9-6-9 in U.S. Soccer's books".
- [ ] Download your chosen voiceover take from ElevenLabs (voice: Rob, about 19.5 seconds)
- [ ] Record 3 vertical clips on your phone, in a quiet spot, with the light in front of you:
  - [ ] Hook, 5 seconds, close up, Haiti jersey
  - [ ] Beat 3, 10 seconds, Haitian flag behind you:
        "Nu Stadium, 4:30 Eastern. Wear the red and blue. Bring your family. Make that stadium sound like home."
  - [ ] Close, 3 seconds, fist up:
        "Follow so you catch my reaction after the final whistle. Ayiti, nou la!"
- [ ] Send Claude the 3 clips and the MP3, or edit them yourself in CapCut using the preview video as the map
- [ ] Make the cover: you, chest up, in the jersey, fired up. "ROAD TO LA" in heavy white type,
      top third, on a Haiti blue background with a red band behind the text
- [ ] Watch the final cut once with the sound off. Every beat should still make sense from the captions.

## Phase 3: Post the preview (Thu Nov 12)

- [ ] Upload to YouTube Shorts with the approved title and cover
- [ ] Description: ask Claude to run /yt-seo for the description and tags
- [ ] Post the same video to TikTok and Instagram Reels
- [ ] For the first hour, reply to comments in your own voice

## Phase 4: Match day (Sat Nov 14)

- [ ] At the stadium or at home, film your own reactions: crowd, flag, your face at key moments.
      Your own footage is safe to use. Broadcast footage is not.
- [ ] Within 3 hours of the final whistle, record the Leg 1 reaction Short using the template
      Claude wrote (win, draw or loss version)
- [ ] Score your hook before you record: python3 hookscore.py --hook "..."
- [ ] Post it the same night

## Phase 5: Leg 2 (Tue Nov 17)

- [ ] Same routine: own footage, reaction Short within 3 hours, posted the same night
- [ ] Use the "through" or "out" version of the Leg 2 template

## Rules that apply to every video

- Only facts with a source. No invented stats, quotes or inside information.
- No match footage, logos or music you do not have the rights to use.
- Hook in the first 2 seconds. No intro.
- One ask per video.
- Banned words are listed in .claude/youtube/voice.md.

## Optional: make Claude faster next time

These need you to change the cloud environment settings, then start a new session:

- [ ] Allow the domain api.creatomate.com and add the secret CREATOMATE_API_KEY, so Claude can render videos
- [ ] Allow the domain elevenlabsusercontent.com, so Claude can download voiceovers directly

## Where everything lives

| Item | Location |
|---|---|
| Voice profile | .claude/youtube/voice.md |
| This guide | .claude/youtube/1804-futbol-launch-guide.md |
| YouTube skills | .claude/skills/yt-* |
| Voiceover takes | Your ElevenLabs account, Text to Speech history |
| Preview video | Sent in your Claude chat |
