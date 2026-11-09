# Revision12 AI vacancy fill QA

Reference research reported AI-labelled moving actors beside vacant/free-play station prompts. This implementation fills vacant application stations with independently authored AI. AI difficulty, exact source replacement rules, and operator configurations remain unknown; this is not a claim of exact commercial behavior.

## Implementation

Player.bot defaults false. Direct Match construction retains its explicit human-only roster; the application opts into Match.fill_vacancies. That method fills up to eight stations with normal simulated actors, marked bot=true/joined=false. It is idempotent, preserves eliminated actors and progress, honors starting lives, and does nothing while paused or finished. Human count/rankings exclude bots. A match ends when all joined humans are eliminated, even with living bots.

Joining a bot station replaces it with a fresh human at zero score, normal starting lives, original gate delay and safe time. The replacement removes that bot's traps/contact cooldowns and releases carried ghosts to eyes mode without teleporting them. Other stations retain their state. Eliminated joined humans cannot rejoin. These replacement details are original policy, not measured cabinet rules.

## Two-pass verification

Seven Match tests cover four maps and 1/2/8-human rosters, replacement, ownership cleanup, no revival/reset, all humans eliminated, sparse joining, configured lives5, gate release, stage carryover and pause/end guards. An eighth actual App test verifies human keyboard input skips AI, normal advancement moves AI without replacing human intent, and taking over a visibly grown AI resets score and radius36 to17 immediately.

Five older tests assumed every unjoined slot was empty or roster length equalled human count. Updated assertions distinguish live bots from joined humans and continue checking human-only rankings/controller input/locators.

Full suite:149 tests passed after fixture migration;150 passed after App integration coverage (23.091s). The strengthened growth-before-takeover assertion subsequently passed all eight bot tests (0.806s). Physical controllers remain deferred. No claim is made about commercial AI strategy or timing equivalence.
