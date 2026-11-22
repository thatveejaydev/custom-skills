---
name: layer-split
description: Split one illustrated frame into layers for animation - a clean expanded background with room for zooms and pans, plus one transparent PNG per character or prop, saved together in a raw folder. Use when the user asks to layer, split or separate an image or scene for animation, parallax or After Effects, or wants a background plate with cutouts. Works with any art style. For storyboarding a whole script, use script-storyboard instead.
---

# Layer Split

Turn one approved frame into pieces that can be animated separately. The frame is the source of truth for style, design and lighting: this skill never restyles it.

## Where files go

**Never save inside a skill folder**, this one or any other. Skill folders are read-only: do not write, copy or download into them, and do not use them as the working directory.

Settle `<output>` **before generating anything**:

1. **The user named a save folder**, now or earlier in this session: `<output>` is that folder. If it is inside a skill folder, say so and ask for another.
2. **A project is open:** `<output>` is `<project>/layered`. The project is the workspace root or working directory the session started in, not this skill's folder and not the folder an input image came from. It does not need to be a git repository. Before using it, always look for a `SKILL.md` in that folder and in each folder above it, even if this skill is installed elsewhere: if there is one, it is a skill folder, not a project.
3. **No project is open:** ask "No project folder is open. Where should I save the layers?" Then stop and wait for the answer. Do not generate, choose a folder or create one first. Use the answer for the rest of the session.

These starting folders count as no project:

- The home folder itself, a drive root, or Desktop, Documents, Downloads, Music, Pictures or Videos themselves. An ordinary folder inside one of them is a project.
- Codex's automatic folders for chats without a project: `Documents/Codex/<date>/...`.
- A skill folder (found by the `SKILL.md` check above, including a source copy of this skill), or anything inside `.codex`, `.agents` or `.claude`.
- System and application folders, such as Windows and Program Files.

Always use absolute paths for `<output>`.

This applies even without an image generation tool, because the prompts include save paths.

## Output

The layers in one `raw` folder, and nothing else:

```text
<output>/<short-scene-name>/
  raw/
    background.png    opaque, 1.5x the frame, with the frame centered
    <name>.png        transparent, one per layer
```

Do not create any other file or folder: no guide copy, previews, manifests, prompt files, import scripts or duplicate layers. If the scene folder already exists, use a new name.

`<skill>` below is the folder containing this file. It is only for running the scripts, never for saving.

## Workflow

### 1. Get an approved frame

Settle `<output>` before this step.

- **The user gives an image:** use it.
- **The user gives only a scene prompt:** create the frame first with the art style skill they named (for example roundhead-toon). Show it and stop until they approve it.

### 2. Plan the layers

Look at the frame and list the layers back to front, each with a short lowercase name. Plan in chat, not in a file.

- Make a layer only for what will move or must overlap something that moves. A held prop stays with its character unless it moves alone. Furniture with someone behind it is its own layer. Everything else stays in the plate.
- Aim for 2-6 layers. Merge distant crowds into one.

Tell the user the layer list, back to front, and the image count (layers + 2, because the background takes two), then continue unless they asked to approve the plan. Above 6 layers, stop and ask first.

### 3. Generate the pieces

Generate every piece as an **edit of the approved frame**, one image per call, with no other style references. In Codex, load the frame with `view_image` before each call, then copy each cutout from `$CODEX_HOME/generated_images/` into `<output>/<short-scene-name>/raw/` as `<name>.png`. The two background images below stay where they were generated: only their merged result goes into `raw/`.

Background plate, at the frame's framing:

```text
Edit this image into an empty background plate. Remove completely: [every layer, described by look and position], including their contact shadows. Paint in what was behind them, continuing the existing shapes, lines and colors, as simple as the rest of the set. Keep everything else identical: camera, framing, aspect ratio, perspective, lighting, linework and shading. Add no characters, objects, detail, texture or text.
```

Expanded background, as an **edit of the background plate** (not of the frame, which still has the characters in it). In Codex, load the plate with `view_image` first:

```text
Zoom out and extend this background on all four sides. The entire input image becomes the central region of the new image, scaled down to exactly two thirds of the width and two thirds of the height, perfectly centered, with one sixth of new scenery on each side. Keep the same aspect ratio. Inside that central region change nothing. Outside it, continue the same place: [what plainly continues above, below, to the left and to the right]. Continue every line at the same angle, thickness and perspective, with the same palette, lighting, linework and shading. Finish any object that was cropped by the edge. Keep the new areas simple and quiet. No border, frame, vignette at the old edge, new focal objects, characters or text.
```

Merge the two. This puts the sharp plate in the middle of the expanded image:

```text
python "<skill>/scripts/expand_background.py" "<plate>" "<expanded>" "<output>/<short-scene-name>/raw/background.png"
```

It needs Pillow and numpy. If it fails, regenerate only the expanded image, at most twice. If it still fails, copy the plate in as `background.png` and tell the user the background is not expanded. Skip the expansion only if the user asks for no extra space.

Cutout:

```text
From this image, isolate only [subject, described by look and position]. Draw it exactly as it appears: same design, pose, angle, expression, colors, linework, shading and lighting direction. Complete any part hidden or cropped in the image: [name those parts]. Remove everything else, including whatever overlaps it. Show one whole subject, large, centered, with clear margin on all sides. Fully opaque subject with crisp outer linework on a genuinely transparent background. No floor, cast shadow, outer glow, blur, border or text.
```

- Keep text that is printed on the subject: replace "or text" with "or any text other than [the words]".
- For an alternate expression or pose, add "Change only [expression or pose]" to the cutout prompt and save it as `<name>-<variant>.png`.
- **If the tool cannot output real transparency,** replace "on a genuinely transparent background" with "on a perfectly flat, solid [color and hex] background, with none of that color on the subject". Use whichever of green #00FF00, magenta #FF00FF or cyan #00FFFF is least like the subject. The check below removes it.
- **If there is no image generation tool,** give the prompts in chat, each headed by the filename to save it as, tell the user to attach the approved frame to each (the plate for the expanded background prompt) and to save the plate and expanded image outside `raw/` and outside any skill folder, and stop. Merge and check when the files are ready.

### 4. Check

```text
python "<skill>/scripts/check_layers.py" "<output>/<short-scene-name>/raw"
```

It needs Pillow and numpy, makes any key-colored layer transparent in place, and creates nothing. Then look at each layer beside the approved frame, without saving previews or composites:

- The background has no trace of a removed subject, no duplicated object, and no visible rectangle or broken line where the original frame's edge was.
- Each design, pose and expression matches, and any printed words are correct.
- No cutout has a fringe, hole or missing part. This includes parts that were outside the frame, which show when zooming out.

Regenerate a failed piece over its own file (for the background, regenerate and merge again), at most twice, then tell the user what is still off.

### 5. Hand off

Give the `raw` folder path and the stacking order, back to front. Give the background's size, and say it goes in centered at 100% scale: at the full 1.5x, the original framing lines up in a 1080x1920 (or 1920x1080) comp, with room to pan or to zoom out to 67%. Say that the cutouts are not positioned or scaled to the frame, and name any effects left out of them (shadows, glow, blur, haze).
