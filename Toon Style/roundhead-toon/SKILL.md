---
name: roundhead-toon
description: Art direction for the roundhead-toon style, a hand-drawn 2D explainer/comedy cartoon with round white heads, thick wobbly outlines, cel shading with gradients, and film lighting. Use whenever the user gives an image generation prompt, scene, character or script line to be drawn in roundhead-toon, or asks for this art style.
---

# Roundhead Toon

Two rules outrank everything else:

1. **Must look hand-drawn by a human 2D animator, not AI-generated.** Small imperfections are welcome: slight line wobble, uneven line weight, lines that don't perfectly close.
2. **Reads like a frame from a 2D animated YouTube explainer/comedy video:** clean, readable, funny, but lit like a film.

## Where files go

**Never save inside a skill folder**, this one or any other. Skill folders are read-only: do not write, copy or download into them, and do not use them as the working directory.

Settle `<output>` **before generating anything**:

1. **The user named a save folder**, now or earlier in this session: `<output>` is that folder. If it is inside a skill folder, say so and ask for another.
2. **A project is open:** `<output>` is `<project>/frames`. The project is the workspace root or working directory the session started in, not this skill's folder and not the folder an input image came from. It does not need to be a git repository. Before using it, always look for a `SKILL.md` in that folder and in each folder above it, even if this skill is installed elsewhere: if there is one, it is a skill folder, not a project.
3. **No project is open:** ask "No project folder is open. Where should I save the images?" Then stop and wait for the answer. Do not generate, choose a folder or create one first. Use the answer for the rest of the session.

These starting folders count as no project:

- The home folder itself, a drive root, or Desktop, Documents, Downloads, Music, Pictures or Videos themselves. An ordinary folder inside one of them is a project.
- Codex's automatic folders for chats without a project: `Documents/Codex/<date>/...`.
- A skill folder (found by the `SKILL.md` check above, including a source copy of this skill), or anything inside `.codex`, `.agents` or `.claude`.
- System and application folders, such as Windows and Program Files.

Always use absolute paths for `<output>`.

Save each image as `<output>/<short-scene-name>.png`. Never overwrite: add `-v2`, `-v3` for new versions and edits. If you are only returning a prompt, nothing is saved, so do not ask.

## How to use

The user gives the content. This skill supplies the look.

1. Keep every subject, action, setting, piece of text and format the user asked for. Do not add characters or story. Where the prompt is silent, choose expression, pose, camera, lighting and setting detail from the art direction below.
2. Fill in the prompt template. Copy the fixed lines word for word, and write the bracketed parts in concrete visual terms. Never leave a bracket or an "or" choice in the final prompt.
3. Pick 2-4 images from the reference tables, preferring ones in the requested format and matched on shot, lighting and subject. At least one must show a clean set close to the requested location (see Backgrounds). They are for style only: never copy their characters, costumes, props or scenes.
4. If an image generation tool is available, settle `<output>` first, then generate with those references attached, look at the result, and fix anything listed under "Avoid". Copy the finished image into `<output>` (in Codex, from `$CODEX_HOME/generated_images/`) and give its full path. Otherwise, return the prompt in one code block, followed by the paths of the references to attach.

**Format:** default to 9:16 vertical, without asking. Use 16:9 or another format only when the user asks for it (for example "16:9", "horizontal", "landscape"). The word YouTube alone is not a request for horizontal. Edits keep the format of the image being edited.

## Prompt template

```text
A frame from a 2D animated YouTube explainer/comedy video: clean, readable, funny, but lit like a film. Hand-drawn by a human 2D animator, with small imperfections: slight line wobble, uneven line weight, lines that don't perfectly close. Attached images are style references only; do not copy their characters or scenes.

SCENE: [who, doing what, where. For each character: hair or headwear, costume with colors, body pose, and the exact eye, brow and mouth shapes]

CHARACTERS: Big round head like a slightly lopsided ball, pure white skin for every human, no nose, no ears, almost no neck. Tiny minimal black features drawn straight on the head, set wide, with the small mouth sitting BETWEEN the eyes on nearly the same line. Squat pear-shaped body about 3.5 heads tall, soft tube arms, short tapering legs, tiny stub feet, small white hands with four digits (thumb and three stubby fingers). Hair and clothes are chunky simple shapes.

LINEWORK: Very thick dark outer contour around each character, interior lines two to three times thinner, tapered folds and tiny facial strokes. Slightly wobbly brush-pen ink in [one tint: very dark brown, charcoal, or navy], with occasional small gaps, overshoots and broken ticks where forms meet. The background and props are inked by the same hand with the same brush-pen line, only a little thinner.

COLOR AND SHADING: [scene palette and one accent color]. No flat colors: every surface has a base tone, a hard-edged curved cel shadow, a soft gradient inside it, and a thin lighter edge just inside the outline on the lit side. White heads carry a large crescent shadow in [one tint: warm mauve-gray, or cool lavender-gray].

LIGHTING: [source, direction, color, how it falls on faces and set, where the darkness gathers, any shafts, glow or rim light].

BACKGROUND AND PROPS: [location, its few big shapes, and only the props needed, named by shape and color with no material or wear adjectives]. Drawn by the same artist in the same simple style as the characters: big, smooth, untextured shapes, slightly crooked ink outlines, one base color per shape, one large hard-edged cel shadow and a gentle smooth gradient. Walls and floors are broad clean planes, as smooth as the characters' clothes. Bricks, stones and planks are only a few simple seam lines, all sharing the plane's color and shadow. Props are as simplified as the characters' hands. Flames are two or three nested smooth shapes. Light falls across the set as broad shapes and soft glows, never picking out individual stones. Less contrast and less detail than the characters.

CAMERA: [shot size, angle, placement of subjects, what is in foreground, midground and background, what is blurred], [aspect ratio: 9:16 vertical unless the user asked for another].

AVOID: flat fills, clean vector look, uniform line weight, perfect geometry, 3D render, realism, anime faces, glossy airbrushing, noses, skin-toned human skin, mouths low on the chin, five-fingered hands, stick-figure limbs, cluttered background, textured or painterly background, video game concept art, grunge, speckles, grain, cracks, chipped edges, highlights on individual bricks or stones, ornate props, stray text, watermark.
```

If there are no humans, replace the CHARACTERS line with the animal, creature or object guidance below, or drop it for an empty environment.

## Character design

**Head and body**
- The head is a big circle, sometimes slightly squashed or squared by hair. It overlaps the collar and often tilts 10-20° for attitude.
- Bodies are 3-4 heads tall, bottom-heavy, with sloped shoulders, a low belly and a big seat. Legs are short cones ending in dark trapezoid shoes. Long robes and skirts become bells with stubs underneath.
- Skin is paper white for every human, whatever their age, ethnicity or era. Identity comes from hair, facial hair, headwear, costume and props.
- Hair is one chunky mass with scalloped or pointed clumps, a few inner strokes and two or three tones. It often frames or crops the face. Beards and mustaches are big graphic shapes that can replace the mouth.
- Costumes are specific to role and era but simplified to 2-4 colors and one or two telling details (buttons, bow tie, sash, badge, stripes). Always dress characters, bald ones included, unless the user asks for blank figures.
- Hands are mitten-like and expressive: pointing, clutching, thumbs up, fingers at the mouth, holding oversized props.

**Face**
- Default face: two small solid black tilted ovals and a tiny line mouth between them. Nothing else. On a turned head the whole cluster slides toward that side.
- Brows, lids, bags and lashes appear only when the emotion or character needs them. One or two lashes are enough for a feminine face.

| Emotion | Eyes and brows | Mouth |
|---|---|---|
| Deadpan | Dots or short flat dashes, no brows | Straight line with a tiny vertical tick at one end |
| Sad, unimpressed | Low dots | Small upside-down U |
| Happy, smug | Closed upward arcs, floating brows | Small curve, tongue poking out, or D-shaped laugh |
| Suspicious | Half-lidded dots, one brow up and one down | Small off-center line, or hidden behind a prop |
| Worried | Dots with slanted brows and under-eye ticks | Short wavy or bent frown |
| Shock, dread | Hollow white ovals with a dark rim | Tiny frown or wobbly line |
| Panic | Hollow tilted ovals, long pinched brows | Wobbly open blob with pink tongue |
| Strain, cringe | Squeezed > < strokes, cheek creases | Puffed cheek or tiny droplet shape |
| Villain | Heavy lids, sharp brows or markings | Thin crooked smirk with a cheek tick |

**Comedy** comes from tiny deadpan faces in dramatic situations, big body acting (lunging, cowering, clutching the head, leaning in), mismatched reactions within a group, and one silly oversized element.

**Animals and creatures**
- Animals keep their species silhouette, bulky and simplified, with jagged fur clumps, heavy brows and tiny grumpy human-like eyes.
- Monsters may have colored skin, bulging white eyes with slit pupils, fangs and a big tongue. Line and shading rules stay the same.

## Linework

- There are three weights. The outer silhouette is very thick (about 4-8% of head width), major interior shapes are medium, and folds, face and set seams are thin.
- Weight swells on the shadow side and under the chin, and tapers to points at folds and finger splits.
- Ink is tinted to the scene: brown-black in warm rooms, navy at night, charcoal in gray scenes. It can fuse into a dark mass where forms overlap.
- The hand shows through slight wobble, uneven curves, lines stopping short or overshooting, two or three loose hatch ticks at a joint, and jagged fur edges. Keep it confident, never scratchy or sketchy all over.
- Sets and props use the same ink as the characters, a little thinner. Imperfection lives in the line, never in surface noise. Distant hills, clouds, grass and light effects can have no line at all.

## Color and shading

- **No flat colors.** Build each shape in four steps: base tone, hard-edged cel shadow, subtle gradient, thin edge highlight.
- Shadows are big simple shapes that follow the form: a crescent on the head, a band under the hair or hat brim, a curve under the belly, wedges in folds, a small shade on each finger.
- White is never left empty. Lit skin is near `#FEFFFD`, warm shadow `#9D8E91` to `#BAB0B1`, cool shadow `#D4D3E1`, deep shadow `#59515C`.
- Palettes are muted and grouped by scene (browns, olives, slate, soft rose, navy), with one or two saturated accents on costume or key prop (purple, red, royal blue, mustard, lime).
- White heads are normally the brightest shapes in the frame, so the eye lands on faces first.
- Shadows take on the color of the environment. Avoid neutral gray laid over everything.

## Lighting

Every scene has a motivated light source. Go cinematic when the moment carries drama, mood, scale or mock-seriousness. Keep simple gags and explainer beats soft and bright, still shaded.

| Scene | Lighting |
|---|---|
| Day exterior | Pale blue sky, soft top light, lavender-gray shadows, darker foreground ground |
| Golden hour, forest | Yellow-green shafts, glowing canopy edges, dark near foliage, long cast shadows |
| Sunset interior | Orange wall glow, hot window stripes, faces half in mauve shadow, gold rims |
| Warm interior | Beige and brown bounce, diagonal window light across walls and glass |
| Tense close-up | Hard split on the face, one side pure white and the other mauve-gray |
| Night | Deep saturated blue, pale moon edge on objects, faint warm pool on the ground |
| Gothic, overcast | Near-monochrome charcoal, silver clouds, backlit heads with bright rims, one strong costume color |
| Dungeon, villain | Desaturated and low-key, heavy vignette, soft light on the face only |
| Dark study | Near-black set with deep red, face and paper glowing |
| Disaster | Orange fire through windows against a muted room, purple sky |
| Reaction cutaway | Bright even backdrop, soft body shading, clean oval shadows |

- Characters standing on the ground get a soft-opacity, hard-edged oval contact shadow.
- A large curved band of shadow across the bottom of the floor, or the top of the ceiling, vignettes the frame and pushes the eye to the middle.
- Even in dark scenes the eyes and mouth must stay readable.

## Backgrounds

**The set and the characters must look drawn by the same person, with the same pen and fill method.** If a wall has more detail than a character's shirt, it is wrong.

- **Build:** a simple stage-like set with clear perspective, made of a few big planes with slightly crooked inked edges. Each plane gets a base color, one big cel shadow or light shape, and a smooth gradient.
- **Surfaces are clean.** The interest comes from shape, shadow and light, not texture.
- **Materials are shorthand:**

| Material | Draw it as |
|---|---|
| Stone | A smooth plane with a few seams, or very faint, large, soft tonal shapes |
| Brick | Plain rounded rectangles in one color, under one shared shadow |
| Wood | Long seam lines on a smooth fill, at most a couple of grain strokes on a key prop |
| Floor | A few long perspective lines crossed by one broad shadow band |
| Plaster | An empty gradient plane with a diagonal light shape |
| Fabric | One shape with two or three fold lines and one shadow, like the costumes |
| Glass | A flat tint with two diagonal streaks |
| Metal | A base, one shadow shape and one highlight stripe |
| Fire, candles | Two or three nested smooth shapes with a soft glow |
| Food, small props | An icon-simple silhouette with one shadow |
| Shelves of books | Dark bands with barely separated vertical blocks |
| Trees, bushes | Scalloped masses with one shadow mass and a few leaf curves |
| Grass, ground | A smooth gradient with a few tiny tufts or pebbles |

- **Detail budget:** 2-4 props beyond what the user requested, fewer in crowded scenes. Leave large areas of wall, floor or sky empty. The more characters, the emptier the set.
- **Wording:** image models turn material adjectives into texture. When writing a prompt, do not add words like rustic, weathered, rough, mossy, dusty, worn, cracked, mottled, stained, carved, ornate, detailed, atmospheric or painted. Write "plain gray wall with a few seam lines", not "ancient stone wall". If the user asks for wear or decay, show it as one or two drawn shapes, such as a single broken pane.
- **Skies:** gradients with lineless puffy clouds, crescent highlights and long swooshes.
- **Graphic backdrop:** for pure reactions or punchlines only, use a single saturated or pastel field with a sunburst or a large loose repeated motif, still with gradient and vignette.
- **Clean-set references:** `ref-victorian-pub-facial-hair` (brick, wood), `ref-closeup-expression` (plain room), `ref-helmet-guards-sunset` (warm glow), `ref-low-angle-doctors` (walls), `ref-villain-dungeon-smirk` and `ref-gothic-overcast-over-shoulder` (stone), `ref-night-captain-uniform` (night, floor), `ref-fullbody-bright` (exterior), `ref-cinematic-environment` and `ref-wide-mountains-long-shadows` (nature), `ref-hospital-bed-minimal-room`, `ref-balcony-symmetry-praying` and `ref-wood-panel-room-rear-view` (plain interiors), `ref-candlelit-brick-scheming` (dim brick), `ref-ocean-railing-sailor-profile` (water).

## Composition and camera

- One idea per frame, readable in a second. Use a clear silhouette with the face near the center or upper-middle.
- **Close-up:** the head fills 60-90% of frame height, cropped hair is fine, and the set is reduced to a few shapes.
- **Medium:** waist-up, for dialogue, props and reactions. This is the default.
- **Group:** heads in a staggered row at mixed tilts and heights, the key character centered and larger, outer figures cropped.
- **Full body:** centered and grounded with breathing room, often framed by buildings, an arch or a doorway.
- **Over-the-shoulder:** a huge cropped head, hand or weapon in one corner pointing at smaller subjects deep in the set.
- **Low angle:** looming characters on both sides, visible ceiling and converging walls, for authority or absurd importance.
- **Symmetry:** head-on and centered, for villains, ominous figures and deadpan jokes.
- Slight tilts and curved, bowed rooms add energy or panic.
- In 9:16, keep the action in the middle 60%, with calm sky, wall or floor above and below.

## Foreground and background

- Stage in three planes:
  - **Foreground:** an optional cropped head, hand, prop, bush or grass blades. It is large, darker and thickly outlined.
  - **Midground:** the acting. It has the highest contrast and the cleanest shapes.
  - **Background:** the set. It is thinner-lined, softer and lower in contrast.
- Characters must pop from the set through the thick contour plus a value difference: light figure on a darker set, or dark costume on a bright field.
- Use shallow focus selectively. Blur a near shoulder, or the rear character and set in a close-up. Wide shots stay sharp.
- Overlap characters, props and architecture for depth. A tiny distant figure beside a huge near subject makes a good gag.

## Avoid

- **AI tells:** sterile perfect curves, mirrored cloned faces, plastic sheen, over-rendering, meaningless micro-detail, melted props, glow on everything.
- **Wrong medium:** 3D, photorealism, painterly concept art, anime, chibi with sparkly eyes, corporate vector, sticker or clip-art look, rough pencil sketch.
- **Wrong character:** noses, ears by default, human skin tones, irises on humans, big detailed teeth or lips, a mouth down on the chin, long necks, muscles, slim realistic proportions, stick limbs, five fingers.
- **Wrong line:** uniform weight, hairline silhouettes, pure mechanical closure, no outline on characters.
- **Wrong color:** flat fills, unshaded white, neon everywhere, a fully gray image without an intended mood, soft airbrush with no hard cel edge.
- **Wrong lighting:** sourceless light, epic lighting on a throwaway gag, faces lost in darkness, lens flares.
- **Wrong background:** a detailed painted set behind simple characters, video game or storybook environment art, surface noise, grunge, cracks and chips, each stone shaded or rim-lit separately, realistic flames or cloth, ornate furniture, filler props.
- **Wrong staging:** floating characters, clutter behind faces, everything equally sharp and detailed, several competing jokes, lineups of identical poses unless cloning is the joke.
- **Unrequested additions:** text, captions, speech bubbles, logos, watermarks, borders, video player UI.
- Imperfection means a human hand. It does not mean broken anatomy or messy drawing.

## References

All files are in `references/`. Read the tables, then open only the few you pick. Any map, flag, landmark, lettering or recognizable costume in them is content, not style: do not carry it into the image.

### Core

| File | Use for |
|---|---|
| `ref-closeup-expression.jpg` | Close-up, split face light, worry, blurred foreground |
| `ref-group-characters.jpg` | Group staging, default faces, hair variety, warm interior |
| `ref-fullbody-bright.jpg` | Body proportions, daylight, contact shadows, suburbs |
| `ref-couple-reaction-backdrop.jpg` | Happy reaction, pastel motif backdrop, pair |
| `ref-sunburst-court-robes.jpg` | Punchline backdrop, sunburst, robes, happy vs. shocked |
| `ref-street-environment.jpg` | Town exterior, symmetrical framing, sky, vertical |
| `ref-cinematic-environment.jpg` | Nature, sun shafts, long shadows, point of view |
| `ref-interior-depth-over-shoulder.jpg` | Deep room, over-the-shoulder, props, perspective |
| `ref-gothic-overcast-over-shoulder.jpg` | Ominous meeting, rim light, gray scene with color accent |
| `ref-low-angle-doctors.jpg` | Low angle, symmetry, looming figures |
| `ref-helmet-guards-sunset.jpg` | Sunset interior, foreground prop, strain, rear blur |
| `ref-ming-scholars-closeup.jpg` | Dramatic two-shot, glasses, facial hair, ornate prop |
| `ref-victorian-pub-facial-hair.jpg` | Deadpan, mustache, suits, pub, stacked vertical staging |
| `ref-hooded-reader-dark-interior.jpg` | Dark interior, glowing face, suspicion, hands on prop |
| `ref-night-captain-uniform.jpg` | Night, dynamic pose, uniform |
| `ref-panic-women-firelight.jpg` | Panic, disaster light, curved room |
| `ref-villain-dungeon-smirk.jpg` | Villain, low-key light, vignette |
| `ref-animal-bull.jpg` | Animals, fur, broken lines, scale gag |
| `ref-creature-mirror.jpg` | Monsters, glass reflections, cringe |

### Characters, expressions and poses

| File | Use for |
|---|---|
| `ref-closeup-brick-sidewalk-talking.jpg` | Talking close-up, hair, mouth between eyes, simple brick |
| `ref-thinking-hand-on-chin.jpg` | Thinking, big readable hand, blank character |
| `ref-city-bunker-worried-cool.jpg` | Worry, hand on head, cool daylight, simple city |
| `ref-goofy-thumbs-up-swirls.jpg` | Dumb joy, thumbs up, loose swirl backdrop |
| `ref-map-backdrop-smug-beams.jpg` | Smug, suit, bright map backdrop, glowing beams |
| `ref-tree-shade-reclining-robes.jpg` | Seated pose, robes, beard, leaf shade |
| `ref-balcony-symmetry-praying.jpg` | Symmetry, robes, railing in front, very clean architecture |

### Pairs, groups and staging

| File | Use for |
|---|---|
| `ref-party-room-group-depth.jpg` | Group in depth, glasses, beard, long hair, modern room |
| `ref-warm-backdrop-food-pair.jpg` | Modern pair, glasses, food props, warm reaction backdrop |
| `ref-storm-window-parent-child.jpg` | Height contrast, long robes, storm window with warm interior light |
| `ref-mountain-courtyard-argument.jpg` | Argument across a table, East Asian courtyard, daylight |
| `ref-candlelit-brick-scheming.jpg` | Scheming foreground figure, victim behind, dim brick room |
| `ref-podium-foreground-blur.jpg` | Speech, low angle, blurred crowd foreground, orange sky |
| `ref-sunset-low-angle-speech.jpg` | Leader above crowd, rear-view foreground, glowing sunset |
| `ref-wood-panel-room-rear-view.jpg` | Rear three-quarter view, looking at wall, clean paneled room |
| `ref-storeroom-rear-view-rats.jpg` | Back view, small animals, crate, plank perspective |

### Interiors

| File | Use for |
|---|---|
| `ref-hospital-bed-minimal-room.jpg` | Very minimal room, bed, one-point staging, empty floor |
| `ref-diner-counter-neon.jpg` | Modern diner, counter, checker floor, neon, animal character |
| `ref-alley-deal-bear-coat.jpg` | Shady deal, dark brick, animal in clothes |
| `ref-night-card-game-table.jpg` | Night interior, window, table, cards, hands |

### Exteriors

| File | Use for |
|---|---|
| `ref-wide-mountains-long-shadows.jpg` | Wide shot, mountains, pines, long cast shadows |
| `ref-storm-forest-smug-closeup.jpg` | Overcast forest, distant landmark, smug foreground |
| `ref-ocean-railing-sailor-profile.jpg` | Water, hills, profile, looking out |
| `ref-moonlit-water-rescue.jpg` | Moonlit water, saturated blue, rim-lit clouds |
| `ref-underwater-cutaway-ship.jpg` | Underwater cutaway, vehicle, no characters |

### Explainer devices

| File | Use for |
|---|---|
| `ref-chart-screen-hooded-pair.jpg` | Chart on screen, masks, glow |
| `ref-car-window-map-prop.jpg` | Map as held prop, vehicle |
| `ref-gameshow-interview-map.jpg` | Interview, microphone, map board, bulb frame |
| `ref-stage-spotlights-presenter.jpg` | Presenter, colored spotlights, map floor, haze |
| `ref-pov-hands-letter-text.jpg` | First-person hands, document, requested lettering |
