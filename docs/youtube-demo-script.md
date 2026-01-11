# Groove Link YouTube Demo Script

## Opening

Making music with software usually means spending a lot of time not making music—clicking through menus, loading plugins, routing audio. Groove Link changes that by connecting Claude Code, an AI assistant that can run commands on your computer, directly to Bitwig Studio, a professional music production application. You describe your song in a simple text file—the tempo, the instruments you want, how they should sound—and Claude builds the entire project for you. This is vibe coding for music production: you focus on creative decisions while the AI handles the technical setup.

## First Prompt

Let's see it in action. Here's a simple request—the kind of thing a producer might type when starting a new track:

> **PROMPT:**
> I want to make a chill instrumental track. Something warm and nostalgic, like a rainy afternoon. Piano as the main instrument, maybe with some soft strings underneath. A simple bass line to hold it together. Around 75 bpm, in a minor key. Nothing too busy—just enough to set a mood.

Notice there's no mention of plugins, no preset names, no signal routing. Just the feeling and the instruments. Claude takes this and figures out the rest—searching through hundreds of available sounds, choosing ones that fit, and wiring everything up in Bitwig.

## Second Prompt

Let's try something completely different. Same workflow, different vision:

> **PROMPT:**
> I'm thinking 80s synthwave. Driving arpeggios, punchy drums, a big lead synth that cuts through. Maybe 118 bpm. I want it to feel like a midnight drive—neon lights, empty highway. Give me something I can build on.

This time the request has more energy, more specificity about the era and texture. But it's still about feel, not file paths. The producer isn't thinking about which folder their drum samples live in—they're hearing the track in their head. Claude bridges that gap. It translates musical intent into the actual technical steps: finding a preset that sounds like "big lead synth," picking drum sounds that fit "punchy," setting up the right tempo. The human stays in the creative space while the machine handles the inventory.

## Third Prompt

One more. This time, something cinematic:

> **PROMPT:**
> I need something dramatic for a short film score. Orchestral, but not cheesy. Low strings building tension, maybe some brass swells. Sparse at first, then it grows. Think modern film composer—Hans Zimmer territory but on a bedroom producer budget. 60 bpm, lots of space.

What's interesting here is how vague and specific coexist. "Hans Zimmer territory but bedroom budget" tells Claude something important: aim high with the sound design, but work with what's actually installed on this machine. The request acknowledges real constraints while still reaching for a vision. And that's the point—this isn't about replacing the producer's ear or judgment. It's about getting to a starting point faster. Once the tracks are there, the real work begins: tweaking, layering, making it yours. Groove Link handles the scaffolding so you can get to the part that actually matters.

## Fourth Prompt

Different direction:

> **PROMPT:**
> Funky. Like a 70s cop show theme but updated. Wah guitar, slap bass, tight drums. Horns if you can find them. Keep it groovy, around 105 bpm. Something you could strut to.

Most producers have thousands of presets installed—synths, samplers, effects—accumulated over years. Sound packs, plugins, factory content. It's a library you own but barely know. You remember the sounds you use often, but the rest just sits there, waiting. Groove Link searches all of it. When you say "wah guitar," it's not guessing—it's scanning your actual installed sounds, matching names and categories, finding what fits. The AI becomes a librarian for your own collection. That's a different kind of value than generating something new. It's helping you use what you already have.

## Fifth Prompt

> **PROMPT:**
> Something ambient and vast. Drones, slow-moving textures, maybe a distant melody that comes and goes. No drums. Like floating through space or sinking underwater. Very slow—50 bpm or less. I want it to breathe.

Ideas are fragile. You hear something in your head—a texture, a mood, a fragment—and it starts slipping away the moment you reach for it. Every click, every menu, every "where did I put that plugin" pulls you further from the original spark. Traditional workflows fight against this. You have to hold the idea in your mind while you do ten minutes of setup. Vibe coding flips that. You capture the idea in words immediately, before it fades, and let the machine catch up. The words become a net. Even if the result isn't exactly what you imagined, you've preserved something—a direction, an anchor. You can refine from there. But you didn't lose the thread.

## Sixth Prompt

> **PROMPT:**
> Lofi hip hop vibes. Dusty drums, a mellow Rhodes or wurlitzer, maybe some vinyl crackle. Something to study to, you know? Laid back, not too busy. 85 bpm feels right.

Under the hood, this is a conversation. Not a form you fill out, not a preset you select from a dropdown—a conversation. You describe what you want. Claude interprets it, makes choices, builds something. If it's not right, you say so. "Swap the Rhodes for something warmer." "Add a subtle bass." "Actually, make it slower." Each exchange gets you closer. That's different from most software, where you either get exactly what you clicked on or you start over. Here, there's room for "almost" and "not quite" and "what if." The interface is language, and language is flexible. It tolerates ambiguity. It lets you think out loud.

## Seventh Prompt

> **PROMPT:**
> Dark techno. Pounding kick, industrial textures, maybe a distorted synth stab. Relentless. Around 130 bpm. Think warehouse at 3am.

So how does this actually work? Claude Code is an AI that can execute commands on your computer—not just answer questions, but do things. Inside Bitwig, there's a custom controller extension listening on a network port, waiting for instructions. Between them, a command-line tool that speaks both languages: it takes requests like "create a track with a distorted synth" and translates them into precise commands Bitwig understands. When Claude searches for "industrial textures," it's running a real search across your installed presets, plugins, sample libraries—fuzzy matching names, filtering by category, ranking by relevance. Nothing is hallucinated. Every sound it loads actually exists on your machine. The AI reasons about what you want; the tooling ensures it maps to reality.

## Eighth Prompt

> **PROMPT:**
> Jazz trio. Upright bass, brushed drums, a warm piano. Intimate, like a small club. Swing feel, around 120 bpm. Keep it classy.

There's a difference between chatting with an AI and working with one. Chat is good for questions and ideas, but it stays in the realm of words. Claude Code crosses into action—it can read files, run commands, build things. And here's what makes that powerful: language models are excellent at understanding what you mean, but they're unreliable at precise, deterministic tasks. They can't perfectly recall every preset in your library or guarantee a file path is correct. But they can write tools that do those things reliably. So that's what happened here. Claude built the search logic, the fuzzy matching, the command-line interface—tools that encode the knowledge of how Bitwig works, where sounds live, what commands to send. The AI wrote code that compensates for its own weaknesses. Now it uses those tools fluently, combining its strength in interpretation with the tool's strength in precision. It's a division of labor: the model reasons, the tool executes.

## Ninth Prompt

Now let's push it. Not a sketch—a full production:

> **PROMPT:**
> I want a complete, radio-ready pop track. Three to four minutes, properly arranged. Verse, chorus, bridge structure. Drums, bass, keys, a main synth lead, maybe pads for atmosphere, and a pluck or arp for movement. Keep the arrangement tight—not everything playing at once, instruments coming in and out so frequencies don't clash. Add shared reverb and delay buses so it sits together. A master chain with gentle compression and limiting. Conservative choices—nothing experimental, just proven sounds that work. I want it to sound like an album track, not a demo. Around 100 bpm, major key, uplifting but not cheesy.

This is where the framework gets tested. We're not asking for three tracks and a vibe anymore—we're asking for a dozen tracks, each with purpose, plus effect buses, plus a master chain, plus ABC notation that understands arrangement. The AI has to think about frequency separation, when instruments enter and exit, how reverb ties things together without muddying the mix. It has to make dozens of choices that a mix engineer would make, and make them conservatively—the goal isn't novelty, it's the sound you've heard a thousand times on the radio. That polished, professional, everything-in-its-place sound. Let's see what it builds.

## Tenth Prompt

Now let's break everything:

> **PROMPT:**
> Make me the worst song you can. Clashing keys, tempos that don't quite work, instruments that have no business being together. Tuba and harpsichord. A recorder playing something annoying. Drums that feel like they're from a different song entirely. Too much reverb on everything. Make it ugly, but committed—like it means it. I want to laugh when I hear it.

The framework doesn't have taste. It doesn't push back and say "actually, a tuba and harpsichord don't pair well." It follows direction. That's not a flaw—it's the point. A tool that only lets you make good choices isn't really a tool, it's a guardrail. Sometimes you want guardrails. Sometimes you want to drive off a cliff on purpose, creatively speaking. The same machinery that assembled a polished pop track a moment ago will now faithfully construct a disaster. And there's something honest about that. It respects your intent, even when your intent is chaos. The human decides what's good. The machine just builds.

## Eleventh Prompt

Now let's try something harder—experimental, but it has to work:

> **PROMPT:**
> I want something genuinely experimental. Unusual time signatures—maybe 7/8 or 5/4. Sounds that don't normally go together but somehow fit. Prepared piano, granular textures, maybe some field recordings. Dissonance that resolves unexpectedly. Sparse, deliberate, architectural. Think Radiohead meets Steve Reich. It should feel strange but intentional, like every weird choice was made on purpose. Make it cohesive even if it's uncomfortable.

There's a difference between breaking rules because you don't know them and breaking rules because you've mastered them. The terrible song was chaos—funny, but chaos. This is something else. This asks the AI to find the edge where unconventional becomes innovative. To pair sounds that shouldn't work and make them work anyway. That's a harder problem. It requires understanding what "cohesive" means even when the ingredients are strange. Whether the result lands or not, the attempt itself is interesting. Can a system built on pattern-matching find patterns in the experimental? Can it understand "deliberate dissonance"? That's not a rhetorical question. Let's find out.

## Twelfth Prompt

Complete genre shift:

> **PROMPT:**
> Blazing fast bluegrass. Like Billy Strings and Earl Scruggs had a baby. Flatpicking acoustic guitar, banjo rolls, upright bass driving hard, maybe a fiddle tearing through the melody. 160 bpm or faster. The kind of thing where your fingers hurt just listening to it. Keep it acoustic, keep it authentic, keep it relentless.

Every genre carries its own physics. Bluegrass isn't just acoustic instruments—it's specific tunings, specific rhythms, specific interplay between players. The banjo rolls behind the melody while the guitar flatpicks over the top. The bass walks but never drags. The fiddle weaves in and out. Getting this right means knowing what "authentic" sounds like for this particular tradition, not just finding instruments with the right names. And speed changes everything—at 160 bpm, the notes blur together, and what matters is the feel, the drive, the forward momentum. Can the system find sounds that belong in this world? Can the notation keep up? Bluegrass doesn't wait around.

## Thirteenth Prompt

Same roots, different soul:

> **PROMPT:**
> An old cowboy tune. The kind of thing Bob Wills or Hank Williams Sr. might sing over. Pedal steel crying in the background, a simple acoustic guitar shuffle, stand-up bass keeping time. Maybe a fiddle, but sweet, not frantic. Slow enough for a story, around 95 bpm. Leave room for a voice that isn't there. Dusty, lonesome, honest.

After all that speed, we slow down. And slowing down is its own challenge. This music exists to frame a voice, to leave space for words. The instruments support—they don't compete. That pedal steel doesn't show off; it aches. The shuffle doesn't push; it sways. Getting this right means understanding restraint, knowing when not to play. It's the opposite of the bluegrass we just heard, even though they share ancestors. Same fiddle, same bass, completely different intention. The system has to feel that difference. Not just slower tempo—a different relationship between the parts. Music that serves the silence as much as the sound.

## Fourteenth Prompt

Now we're forming a superband:

> **PROMPT:**
> Iggy Pop's "Passenger" meets The Clash doing "Lost in the Supermarket" meets Violent Femmes meets Talking Heads. All of them in a room together, forming a new band. Driving but angular. Acoustic but electric. That nervous post-punk energy, like the song might fall apart but never does. Biting bass line, jangly guitars, drums that push and stutter. 140 bpm, restless, smart, a little dangerous. New wave with dirt under its fingernails.

This is a different kind of prompt—not a genre, but a collision. Four distinct artists, each with their own vocabulary, mashed into one hypothetical band. The system has to understand what makes each of them tick: Iggy's hypnotic drive, The Clash's melodic punk, the Femmes' acoustic rawness, Talking Heads' anxious angularity. Then it has to find the common thread and pull. That's not retrieval—that's synthesis. It's asking the AI to hear music that doesn't exist yet, to imagine a room where these influences meet and make something new. Whether it works or not, the attempt reveals something about how the system thinks about style, influence, and the spaces between genres.

## Fifteenth Prompt

Two sides of electronic darkness:

> **PROMPT:**
> Depeche Mode meets Nine Inch Nails. The cold precision of "Enjoy the Silence" crashing into the industrial chaos of "Closer." Atmospheric synths layered over distorted, mechanical beats. Beautiful and broken at the same time. Dark pads, crunchy textures, a bassline that feels like a threat. Polished surfaces hiding something violent underneath. 110 bpm, brooding, intense, like a machine having a nightmare.

These two share more DNA than it might seem. Trent Reznor grew up on Depeche Mode; you can hear it in the quieter moments of Nine Inch Nails. But where Depeche Mode stays elegant, NIN tears things apart. One is seduction, the other is confrontation. Putting them together asks: what lives in between? Can you have polish and destruction in the same track? Synths that shimmer and synths that shred? The AI has to balance these tensions—not just pick sounds from both camps, but find a middle ground that honors both. Restraint and aggression. Melody and noise. That's a tightrope, and the interesting music lives right there on the wire.

## Sixteenth Prompt

This one already happened once:

> **PROMPT:**
> Nirvana meets Lead Belly. "In the Pines"—that old murder ballad, dragged through the Pacific Northwest mud. Acoustic guitar, dark and droning, but with that grunge weight underneath. Raw, desperate, haunted. Like a ghost story told by someone who's lived it. Simple arrangement, overwhelming emotion. The kind of quiet that's louder than screaming. 70 bpm, minor key, no escape.

Kurt Cobain actually did this—his MTV Unplugged version of "Where Did You Sleep Last Night" is one of the most devastating performances ever recorded. So this prompt isn't hypothetical. It's asking the system to find that same territory: where a song from the 1870s, filtered through Lead Belly in the 1940s, becomes a 1990s grunge confession. Three generations of American pain in the same room. The interesting question isn't whether the AI knows the history—it's whether it understands what these artists share beneath the surface. The rawness. The refusal to polish the edges. The sense that the song is barely being held together. That's not a genre. That's an emotional frequency.

## Seventeenth Prompt

Quieter now:

> **PROMPT:**
> M. Ward meets Noah Kahan. That dusty, lo-fi warmth from another era mixing with the earnest, heart-on-sleeve folk-pop of right now. Acoustic guitar with tape hiss, maybe some soft piano, a melody you can't get out of your head. Nostalgic but present. Vermont winters and California sunsets somehow in the same song. Intimate, unhurried, the kind of music that sounds like a letter from a friend. 90 bpm, gentle, sincere.

Both of these artists write like they're telling you a secret. M. Ward buries it in reverb and vintage haze; Noah Kahan says it straight to your face. Different eras, different coasts, but the same core impulse: be honest, keep it simple, let the song breathe. This pairing asks whether sincerity has a sound—whether you can blend the weathered and the fresh and still feel like one person is singing. Folk music keeps reinventing itself, generation after generation, and somehow stays recognizable. The names change, the production changes, but that impulse to sit down with a guitar and say something true—that thread runs through all of it.

## Eighteenth Prompt

This one might start an argument:

> **PROMPT:**
> Louis Armstrong meets Kenny G. The founding father of jazz improvisation shaking hands with smooth jazz's most polarizing figure. Trumpet and soprano sax trading lines over a warm, swinging rhythm section. Melodic, accessible, joyful. Find what they share instead of what divides them. Something your grandparents and your dentist's waiting room could both love. 100 bpm, major key, no attitude—just music that wants to make you smile.

Jazz purists will hate this prompt. Kenny G represents everything they think went wrong—the smoothing of edges, the commercial polish, the elevator music reputation. But here's the thing: Louis Armstrong was a populist too. He wanted everyone to love his music, not just critics. He smiled on stage. He made hits. He brought jazz to people who'd never heard it. Both of these artists, in their own way, chose accessibility over exclusivity. The system doesn't carry opinions about who belongs in the canon. It just looks for common ground. And sometimes that's clarifying—it finds connections that snobbery might miss.

## Nineteenth Prompt

Forget the artists. Give me a context:

> **PROMPT:**
> A high school marching band. Brass section blaring, snare drums cracking, the whole thing a little rough around the edges but full of heart. Fight song energy. Something you'd hear crossing a football field on a Friday night in October. Trumpets, trombones, sousaphone holding down the bottom, maybe a glockenspiel cutting through. 120 bpm, straight eighths, loud and proud. It doesn't have to be perfect—it has to be alive.

Not every prompt is about blending influences or finding new territory. Sometimes you just want to evoke a place, a feeling, a memory. The smell of cut grass and hot dogs. The stands full of parents. The drumline leading the band onto the field. This kind of music isn't about virtuosity—it's about belonging. Everyone playing together, not perfectly, but together. The system can do this too. It's not always about innovation. Sometimes it's about capturing something familiar so accurately that you feel like you're back there, seventeen years old, watching the halftime show, not knowing yet how much you'd miss it.

## Twentieth Prompt

Same brass, different soul:

> **PROMPT:**
> A Tremé second line. New Orleans brass band, rolling down the street, umbrellas in the air. Sousaphone laying down that bounce, snare drum popping syncopation, trumpets and trombones calling and responding. The rhythm that makes you move whether you want to or not. Joyful and mournful at the same time—celebration and funeral in the same breath. 95 bpm but it swings so hard it feels faster. Music for the living and the dead.

This is music that can't be separated from its place. It belongs to the streets of New Orleans, to the neighborhoods, to the tradition of honoring the dead by dancing them home. You can't bottle it. You can't fully recreate it in a studio. But you can reach for it—capture some of that rhythm, that call and response, that feeling of a whole community moving together. The marching band we heard before was suburban, Friday night, football. This is urban, Sunday afternoon, sacred and profane at once. Same instruments. Completely different gravity. The prompt isn't just asking for a sound—it's asking for a culture. That's a lot to carry. Let's see how close we can get.

## Twenty-First Prompt

Older than all of this:

> **PROMPT:**
> A Native American ritual. Drums like a heartbeat, steady and deep. Wooden flute carrying a melody that feels ancient. Voices rising and falling together, not performing but praying. Sparse, patient, connected to the earth. No tempo in the modern sense—time measured differently. Music that isn't entertainment. Music that's ceremony. Respect it.

We should be careful here. This isn't a genre to sample or a style to borrow. It's sacred tradition, and no DAW can recreate what happens in a ceremony passed down through generations. The prompt knows that—it says "respect it." What we can do is gesture toward it, acknowledge it, maybe find sounds that honor rather than appropriate. The system will do its best with the flutes and drums it can find. But the commentary matters more than the output. Some music exists for purposes we can only witness from the outside. The framework can evoke many things, but it can't replace what isn't ours to take. It can only point toward it with humility.

## Twenty-Second Prompt

Three songs walk into a room:

> **PROMPT:**
> Son Volt's "Windfall" meets Townes Van Zandt's "Highway Kind" meets John Prine's "Boundless Love." Three generations of American songwriting sitting on the same porch. Acoustic guitar, maybe a pedal steel sighing in the distance, a bass that knows when to stay quiet. Lyrics you can see—highways, dust, love that endures. Weary but not defeated. Midwest longing, Texas wandering, and that Prine warmth holding it all together. 85 bpm, country waltz feel, songs for driving alone at night.

This is a prompt about lineage. Townes wrote songs that felt like they'd always existed. Prine could break your heart and make you laugh in the same verse. Jay Farrar carried that Midwest ache into alt-country and never let go of it. They didn't all know each other, but they're in conversation anyway—across decades, across state lines, through the songs themselves. When you name specific tracks, you're asking the system to understand not just artists but moments. The quiet resolve of "Windfall." The restless poetry of "Highway Kind." The late-life grace of "Boundless Love." Can a machine find where those three songs overlap? Somewhere out there on a long road, maybe it can.

---

## Closing

So what have we seen?

Twenty-two prompts. Chill piano to blazing bluegrass. Radio-ready pop to intentional disaster. Jazz legends to high school marching bands. Sacred ritual to punk rock superbands. Each one typed in plain language by someone who knows what they want to hear but doesn't want to spend an hour setting it up. Each one translated—by Claude, by the tools Claude built, by the framework connecting them to Bitwig—into actual tracks, actual instruments, actual projects you can open and play and build on.

That's what Groove Link does. But the how matters as much as the what.

This project wasn't planned in a design document. It was built through conversation. I described what I wanted; Claude wrote code. When the code didn't work, I described what went wrong; Claude fixed it. When Bitwig's API had quirks—and it has many—we figured them out together, adding logging, reading documentation, adjusting approaches until things connected. The controller extension, the command-line tools, the search logic, the fuzzy matching, the protocol layer—all of it emerged from dialogue. Vibe coding isn't a marketing term. It's a method. You describe intent; the machine writes implementation. You stay in the creative space; the machine handles the technical overhead.

But here's what makes this different from chat.

Chat is passive. You ask a question, you get an answer, you copy-paste it somewhere and hope it works. Claude Code is active. It reads your files. It runs commands. It builds things that persist after the conversation ends. When I said "search my installed presets," Claude didn't describe how to do it—it wrote a tool that does it, tested it, refined it, and now that tool exists. I use it every day. The AI created infrastructure, not just information.

And that changes what's possible.

A year ago, I would have spent weeks building this. Reading Bitwig's API documentation line by line. Writing Java I'd forget the syntax of. Debugging TCP connections with packet sniffers. Instead, I spent that time describing what I wanted and iterating on results. The friction collapsed. Not because the work got easier—the work is the same, someone has to write the code, someone has to debug the protocol—but because the labor shifted. I focused on architecture, on user experience, on what the tool should feel like. Claude focused on implementation details, on syntax, on the thousand small decisions that don't require taste but do require precision.

That's the division of labor we talked about earlier. The human reasons about what matters; the machine handles what's mechanical. And the machine is honest about its limits. It writes tools to compensate for the things it can't do reliably—like remembering every preset path, or guaranteeing a file exists. The tools encode knowledge. The AI uses them. Together, they're more capable than either alone.

Now extrapolate.

Today, Claude Code is the interface. I type prompts in a terminal; music appears in Bitwig. But what happens when the interface disappears further? When you don't type at all—you hum a melody, or sketch a waveform, or just say "something like this but sadder"? The gap between intent and execution keeps shrinking. The tools keep getting better at understanding vague, human, incomplete descriptions and turning them into precise, functional output.

Next year, the models will be smarter. They'll hold more context, make fewer errors, need less hand-holding. The tools they build will be more sophisticated—not just fuzzy search, but semantic understanding of what "warm" means for a piano tone or what "driving" means for a drum pattern. The loop between "I want" and "here it is" will tighten. And the interesting question isn't whether AI will replace musicians—it won't, because music is human expression and humans will always want to express—but whether AI will replace the mechanical parts of music production so thoroughly that the barrier to entry vanishes.

What happens when anyone can produce an album-quality track by describing it?

The same thing that happened when anyone could publish a book, or shoot a film, or broadcast to the world. More voices. More noise. More brilliance buried in the avalanche. The tools democratize; the taste differentiates. Groove Link doesn't make you a better musician. It just gets the gear out of the way so you can find out if you have something to say.

And further out—when AI improves AI faster than humans can?

We're not there yet. But we're closer than most people think. The models are already writing code that extends their own capabilities. Claude built the tools that Claude uses. That's a loop. Right now, humans are still in that loop—directing, correcting, deciding what matters. But the loop is tightening. The human contribution is shifting from implementation to judgment, from labor to taste, from doing to choosing.

That's not a threat. It's a transition. The same transition that happened when we stopped hand-copying manuscripts and started printing books. When we stopped developing film in darkrooms and started editing pixels. The work doesn't disappear—it transforms. The people who thrive are the ones who understand what the new tools can do and use them to make things that couldn't exist before.

This demo was twenty-two prompts and a lot of music. But underneath it was something else: a proof that the way we build things is changing. Not someday. Now. The conversation is the interface. The AI is the infrastructure. The human is the one with something to say.

So say something.

---

*Groove Link is open source. The tools, the extension, the framework—all of it available to use, extend, break, and rebuild. Because the best way to understand where this is going is to build something yourself and feel the future arrive under your fingertips.*
