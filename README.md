# This is a simple implementation of the Chip8 interpreter

- Originally I started implementing this myself, learning about the Chip8 instruction set and it's history
    -- Thanks by the way to this repository, that does a great job at presenting the Chip8 instruction set: https://github.com/mattmikolay/chip-8

- After learning how it works and how I could do it, it just became sort of just tedious grunt work.
- Recently google made it's Gemini 3.1 model available and Google's Antigravity IDE (see https://antigravity.google/) caught my attention.
- I was curious and wanted to see how fast I could implement this interpreter/emulator with the help of AI agents. This was my experience
 
 # How I started
- I started out by letting the agent create a implementation plan, which I then created in a dedicated file, you can find here in this repo (implementation_plan.md). I did modify some aspects, because it added requirements I didn't deem necessary for my use case and also some private references in my system, but generally this was what I worked with.
 
 # Experience/Final Result
 - I was kinda impressed. I got the emulator running in about 20 minutes.
 - Skimming through the code, it made sense to me how it was implemented, especially since it kinda looked very similar in how I implemented it (since I started implementing it myself already).
 - All around, the generation of the interpreter, the review and finishing up to release this in a public repo took me around 1 to 2 hours.
 - That said, this shouldn't be taken as a serious implementation, because for that I would do a more in depth review of this code and I wouldn't confidently say that I was 100% thorough here. This is just me trying out AI development with Google's Antigravity IDE (free plan).
 - Not everything went smooth, e.g. it originally had some roms in it's implementation plan that it wanted to test against and couldn't load them but still reported that part as successfull. But still, mostly everything seem to work smooth.
 - I just did a very simple test and only tested with this rom: https://github.com/mattmikolay/chip-8/tree/master/cavern. Further scrutiny of this code would potentially reveal more issues.
 - Also, I think one negative side effect of doing this kind of development: I do think if you don't understand the problem and possible solutions, it's takes away this learning if you overrely on an AI agent. Since it's kind of fun vibe coding away I thik it's quite easy to loose track of what your app even actually does and, even worse, not even have learned the problem and what the solution to it actually is. "What I cannot create, I do not understand".
