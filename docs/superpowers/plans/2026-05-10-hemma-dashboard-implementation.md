# Hemma Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a third Lovelace dashboard `Hemma` to `homeassistant/config/`, adopting the upstream Hemma look-and-feel with 4 views (Home, Bedroom, Living Room, Office) mapped to the user's existing devices.

**Architecture:** Copy Hemma's templates, theme, helpers package, and `www/` assets verbatim from `/tmp/Hemma/` (already cloned). Customise `packages/hemma_helpers.yaml` and `dashboards/templates/includes/hemma_navbar_mobile.yaml` to user's entity IDs and view paths. Author new `dashboards/hemma/hemma.yaml` mapping user's lights, climate, fan, vacuum, sensors, and media players. Register dashboard in `configuration.yaml`. User performs HACS card install + Lovelace resource registration via UI as final manual step.

**Tech Stack:** Home Assistant 2025.x (storage-mode Lovelace + YAML named dashboards), HACS custom cards (button-card, navbar-card, browser_mod, more-info-card, mushroom, uix), bash/zsh for file ops.

**Source-of-truth references (open these in any task that needs verification):**
- Spec: `docs/superpowers/specs/2026-05-09-hemma-dashboard-design.md`
- Upstream Hemma clone: `/tmp/Hemma/`
- Upstream example dashboard: `/tmp/Hemma/dashboards/hemma/hemma.yaml.example`
- Upstream README: `/tmp/Hemma/README.md`

**Convention:** All paths absolute. Working dir for commands: `/Users/sergeikharchikov/dev/personal/pi-setup`.

---

## Task 1: Pre-flight verification

**Files:**
- Inspect: `/tmp/Hemma/` (must be present)
- Inspect: `/Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/configuration.yaml`

- [ ] **Step 1: Verify Hemma upstream clone exists**

Run: `test -d /tmp/Hemma/dashboards/templates/button_cards/cards && echo OK || echo MISSING`
Expected: `OK`

If `MISSING`, run: `git clone --depth 1 https://github.com/willsanderson/Hemma.git /tmp/Hemma`

- [ ] **Step 2: Verify expected upstream files exist**

Run:
```bash
for f in \
  /tmp/Hemma/dashboards/hemma/hemma.yaml.example \
  /tmp/Hemma/dashboards/templates/includes/hemma_navbar_mobile.yaml \
  /tmp/Hemma/dashboards/templates/includes/hemma_screen_layout.yaml \
  /tmp/Hemma/dashboards/templates/includes/hemma_entity_layout.yaml \
  /tmp/Hemma/dashboards/templates/includes/hemma_navigation.yaml \
  /tmp/Hemma/themes/hemma/hemma.yaml \
  /tmp/Hemma/packages/hemma_helpers.yaml \
  /tmp/Hemma/www/layout-card-modified/layout-card-modified.js \
  /tmp/Hemma/www/navbar-popup-caret/navbar-popup-caret.js \
  /tmp/Hemma/www/navbar-sidebar-offset/navbar-sidebar-offset.js \
  /tmp/Hemma/www/hemma/rooms/home.jpg \
  /tmp/Hemma/www/hemma/rooms/home-night.jpg \
  /tmp/Hemma/www/hemma/rooms/bedroom.jpg \
  /tmp/Hemma/www/hemma/rooms/livingroom.jpg \
  /tmp/Hemma/www/hemma/icons/home.svg; do
  test -e "$f" || echo "MISSING: $f"
done; echo "DONE"
```
Expected: `DONE` with no `MISSING` lines.

- [ ] **Step 3: Verify clean git state**

Run: `git -C /Users/sergeikharchikov/dev/personal/pi-setup status --porcelain`
Expected: empty output (clean working tree).

If not clean, stop and inform user.

- [ ] **Step 4: Confirm current branch**

Run: `git -C /Users/sergeikharchikov/dev/personal/pi-setup rev-parse --abbrev-ref HEAD`
Expected: `main`

---

## Task 2: Copy `button_cards/` templates verbatim

**Files:**
- Create: `homeassistant/config/dashboards/templates/button_cards/{badges,base,cards,popups}/` (entire subtree)

- [ ] **Step 1: Create target dir**

Run: `mkdir -p /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/button_cards`

- [ ] **Step 2: Copy all four subdirs verbatim**

Run:
```bash
cp -R /tmp/Hemma/dashboards/templates/button_cards/badges \
      /tmp/Hemma/dashboards/templates/button_cards/base \
      /tmp/Hemma/dashboards/templates/button_cards/cards \
      /tmp/Hemma/dashboards/templates/button_cards/popups \
      /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/button_cards/
```

- [ ] **Step 3: Verify file counts match upstream**

Run:
```bash
cd /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/button_cards
echo "badges: $(ls badges | wc -l) (expect 10)"
echo "base:   $(ls base   | wc -l) (expect 9)"
echo "cards:  $(ls cards  | wc -l) (expect 16)"
echo "popups: $(ls popups | wc -l) (expect 3)"
```
Expected: counts match parenthesised expectations.

---

## Task 3: Copy verbatim `includes/` files (3 of 4)

**Files:**
- Create: `homeassistant/config/dashboards/templates/includes/hemma_screen_layout.yaml`
- Create: `homeassistant/config/dashboards/templates/includes/hemma_entity_layout.yaml`
- Create: `homeassistant/config/dashboards/templates/includes/hemma_navigation.yaml`

- [ ] **Step 1: Create includes dir**

Run: `mkdir -p /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes`

- [ ] **Step 2: Copy three verbatim includes (NOT the navbar)**

Run:
```bash
cp /tmp/Hemma/dashboards/templates/includes/hemma_screen_layout.yaml \
   /tmp/Hemma/dashboards/templates/includes/hemma_entity_layout.yaml \
   /tmp/Hemma/dashboards/templates/includes/hemma_navigation.yaml \
   /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/
```

- [ ] **Step 3: Verify files present, navbar NOT yet present**

Run:
```bash
cd /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes
ls
```
Expected output (exactly 3 files):
```
hemma_entity_layout.yaml
hemma_navigation.yaml
hemma_screen_layout.yaml
```

`hemma_navbar_mobile.yaml` is intentionally missing — it's edited in Task 8.

---

## Task 4: Copy theme + helpers package + www tree

**Files:**
- Create: `homeassistant/config/themes/hemma/hemma.yaml`
- Create: `homeassistant/config/packages/hemma_helpers.yaml` (will be edited in Task 7)
- Create: `homeassistant/config/www/hemma/` (entire subtree)
- Create: `homeassistant/config/www/layout-card-modified/layout-card-modified.js`
- Create: `homeassistant/config/www/navbar-popup-caret/navbar-popup-caret.js`
- Create: `homeassistant/config/www/navbar-sidebar-offset/navbar-sidebar-offset.js`

- [ ] **Step 1: Create target dirs**

Run:
```bash
mkdir -p /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/themes/hemma \
         /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/packages \
         /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/www
```

- [ ] **Step 2: Copy theme**

Run: `cp /tmp/Hemma/themes/hemma/hemma.yaml /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/themes/hemma/hemma.yaml`

- [ ] **Step 3: Copy helpers package (verbatim — edits come in Task 7)**

Run: `cp /tmp/Hemma/packages/hemma_helpers.yaml /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/packages/hemma_helpers.yaml`

- [ ] **Step 4: Copy www subtrees**

Run:
```bash
cp -R /tmp/Hemma/www/hemma \
      /tmp/Hemma/www/layout-card-modified \
      /tmp/Hemma/www/navbar-popup-caret \
      /tmp/Hemma/www/navbar-sidebar-offset \
      /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/www/
```

- [ ] **Step 5: Verify www/hemma subtree has rooms + icons + fonts**

Run:
```bash
cd /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/www/hemma
test -f rooms/home.jpg && test -f rooms/home-night.jpg && \
test -f rooms/bedroom.jpg && test -f rooms/livingroom.jpg && \
test -f icons/home.svg && test -f fonts/hanken-grotesk.css && echo OK
```
Expected: `OK`

If `fonts/hanken-grotesk.css` is missing, list `fonts/`: `ls /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/www/hemma/fonts` and adjust the resource URL in Task 9 step 3 accordingly.

---

## Task 5: Commit 1 — verbatim asset copy

- [ ] **Step 1: Stage all new asset files**

Run:
```bash
cd /Users/sergeikharchikov/dev/personal/pi-setup
git add homeassistant/config/dashboards/templates/button_cards/ \
        homeassistant/config/dashboards/templates/includes/ \
        homeassistant/config/themes/hemma/ \
        homeassistant/config/packages/hemma_helpers.yaml \
        homeassistant/config/www/
```

- [ ] **Step 2: Verify staged file count**

Run: `git diff --cached --stat | tail -1`
Expected: roughly `100+ files changed, ... insertions(+)` (Hemma ships ~80 SVGs + templates + theme + JS = 100+ files).

- [ ] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
homeassistant: copy Hemma assets verbatim

Templates, theme, helpers package (unedited), and www subtree from
upstream willsanderson/Hemma. Helpers + navbar will be customised in
the next commit.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: Verify commit**

Run: `git log --oneline -1`
Expected: shows the commit message starting with `homeassistant: copy Hemma assets verbatim`.

---

## Task 6: Verify HA config still parses (no Hemma-specific changes yet)

This is a sanity check before customisation.

**Files:**
- No changes — just inspection.

- [ ] **Step 1: Check that the assets sitting in `themes/`, `packages/`, `www/` haven't been wired into `configuration.yaml` yet**

Run: `grep -n "packages:\|hemma" /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/configuration.yaml`
Expected: only matches inside the comment line `# Lovelace: default + map stay UI-managed; named dashboards are YAML` (i.e., no real `packages:` entry, no `hemma` references).

- [ ] **Step 2: If a Home Assistant instance is reachable, run check-config**

If `ha` CLI is available locally and HA is running, run: `ha core check`
Expected: `Configuration is valid` or equivalent.

If not available, skip — we'll re-run check after Task 9.

---

## Task 7: Customise `packages/hemma_helpers.yaml`

**Files:**
- Modify: `homeassistant/config/packages/hemma_helpers.yaml`

- [ ] **Step 1: Replace `hemma_motion_living_room.initial`**

Edit `/Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/packages/hemma_helpers.yaml`.

Old:
```yaml
  hemma_motion_living_room:
    name: "Hemma Motion - Living Room"
    initial: "binary_sensor.living_room_hub_motion"
```

New:
```yaml
  hemma_motion_living_room:
    name: "Hemma Motion - Living Room"
    initial: "binary_sensor.human_presence_sensor_2"
```

- [ ] **Step 2: Replace `hemma_motion_bedroom.initial`**

Old:
```yaml
  hemma_motion_bedroom:
    name: "Hemma Motion - Bedroom"
    initial: "binary_sensor.hue_motion_sensor_motion"
```

New:
```yaml
  hemma_motion_bedroom:
    name: "Hemma Motion - Bedroom"
    initial: "binary_sensor.tze200_3towulqd_ts0601_occupancy"
```

- [ ] **Step 3: Leave `hemma_motion_kitchen.initial` empty**

Verify it already reads:
```yaml
  hemma_motion_kitchen:
    name: "Hemma Motion - Kitchen"
    initial: ""
```

No edit needed — kitchen view doesn't exist; blank disables the badge.

- [ ] **Step 4: Switch `input_number.hemma_thermostat_target_temperature` to °C**

Old:
```yaml
  hemma_thermostat_target_temperature:
    name: Thermostat Target Temperature
    # Celsius users: min: 15, max: 30, step: 0.5, unit_of_measurement: "°C"
    min: 68
    max: 75
    step: 1
    unit_of_measurement: "°F"
    mode: slider
```

New:
```yaml
  hemma_thermostat_target_temperature:
    name: Thermostat Target Temperature
    min: 15
    max: 30
    step: 0.5
    unit_of_measurement: "°C"
    mode: slider
```

- [ ] **Step 5: Switch `input_select.hemma_thermostat_mode.initial` to `heat`**

Old:
```yaml
  hemma_thermostat_mode:
    name: Thermostat Mode
    options:
      - cool
      - heat
    initial: cool
```

New:
```yaml
  hemma_thermostat_mode:
    name: Thermostat Mode
    options:
      - cool
      - heat
    initial: heat
```

- [ ] **Step 6: Verify all 5 edits applied**

Run:
```bash
cd /Users/sergeikharchikov/dev/personal/pi-setup
grep -n "binary_sensor.human_presence_sensor_2\|binary_sensor.tze200_3towulqd_ts0601_occupancy\|min: 15\|max: 30\|initial: heat" homeassistant/config/packages/hemma_helpers.yaml
```
Expected: 5 lines, one per edit.

---

## Task 8: Copy + customise `hemma_navbar_mobile.yaml`

**Files:**
- Create: `homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml`

The upstream file is 1628 lines with three navbar sections (phone portrait ~line 480, tablet portrait ~line 1020, tablet landscape ~line 1540). All three need the same logical edits: drop Kitchen, drop Rooms popup, drop Scenes popup, add Office as a flat link with `home.svg` icon as placeholder.

Strategy: copy upstream verbatim, then edit each section.

- [ ] **Step 1: Copy navbar verbatim as starting point**

Run: `cp /tmp/Hemma/dashboards/templates/includes/hemma_navbar_mobile.yaml /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml`

- [ ] **Step 2: Locate the three navbar route blocks**

Run:
```bash
grep -n "label: Rooms\|label: Scenes\|/dashboard-hemma/kitchen\|/dashboard-hemma/living-room\|/dashboard-hemma/bedroom\|/dashboard-hemma/home" \
  /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml
```

Note line numbers — edits in subsequent steps reference these.

- [ ] **Step 3: Replace `/dashboard-hemma/kitchen` route entries with `/dashboard-hemma/office`**

Use Edit/sed to globally replace the kitchen ROUTE (not the icon mapping JS lines). Run a careful sed that only swaps `url:` lines:

```bash
sed -i.bak -E '/^[[:space:]]+- url: \/dashboard-hemma\/kitchen$/{
  N
  s|- url: /dashboard-hemma/kitchen\n([[:space:]]+)image: /local/hemma/icons/kitchen.svg|- url: /dashboard-hemma/office\n\1image: /local/hemma/icons/home.svg|
}' /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml
```

Then verify no remaining `/dashboard-hemma/kitchen` route references in `url:` lines:
```bash
grep -n "url: /dashboard-hemma/kitchen" /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml
```
Expected: empty.

If sed didn't work cross-platform on macOS (BSD sed), use the Edit tool manually for each occurrence — three sites, around lines 549, 1051, 1573 (verify with grep from Step 2).

- [ ] **Step 4: Update icon-mapping JS blocks to drop Kitchen**

Find blocks like:
```js
if (p === '/dashboard-hemma/kitchen') return '/local/hemma/icons/kitchen.svg';
```

These appear at lines ~507, ~515, and possibly others. Replace each with:
```js
if (p === '/dashboard-hemma/office') return '/local/hemma/icons/home.svg';
```

Verify after edits:
```bash
grep -n "dashboard-hemma/kitchen" /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml
```
Expected: empty.

- [ ] **Step 5: Remove the "Rooms" dropdown popup (phone-portrait section, ~line 501)**

Locate the block starting with `- label: Rooms` in the phone-portrait section. The full block is approximately lines 501–562 (verify with grep from Step 2). Delete the entire block (from `- label: Rooms` through the closing of its `popup:` structure, ending just before the next `# Scenes` or `# ` comment marker).

Use Read + Edit: open lines 495–570, identify the boundary, delete the block.

After delete, verify:
```bash
grep -n "label: Rooms" /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml
```
Expected: empty.

- [ ] **Step 6: Add a flat Bedroom + Office route to phone-portrait section where Rooms popup used to be**

Insert directly where the Rooms popup was deleted:
```yaml
        - url: /dashboard-hemma/bedroom
          image: /local/hemma/icons/bedroom.svg
        - url: /dashboard-hemma/living-room
          image: /local/hemma/icons/living-room.svg
        - url: /dashboard-hemma/office
          image: /local/hemma/icons/home.svg
```

(YAML indentation must match the surrounding `routes:` list — typically 8 spaces. Verify by inspecting neighboring entries.)

- [ ] **Step 7: Remove Scenes popup blocks in all three sections**

Locate `- label: Scenes` blocks (lines ~563, ~1068, and the equivalent in the tablet-landscape section). Delete each block from `- label: Scenes` through the end of its `popup:` structure.

After delete, verify:
```bash
grep -n "label: Scenes\|/dashboard-hemma/scenes" /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml
```
Expected: empty.

- [ ] **Step 8: Confirm tablet-portrait + tablet-landscape sections also have Office**

In each of those sections (which use flat route lists, not popups — see grep results from Step 2 for line numbers around 1032 and 1555), confirm Step 3's sed replaced kitchen → office. If not, manually add an Office entry mirroring the pattern of the Living Room entry.

Verify final state:
```bash
grep -c "url: /dashboard-hemma/office" /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml
```
Expected: at least `3` (one per navbar section).

- [ ] **Step 9: Delete the sed backup file**

Run: `rm -f /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml.bak`

- [ ] **Step 10: YAML lint**

Run:
```bash
python3 -c "import yaml,sys; yaml.safe_load(open('/Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml'))" && echo OK
```
Expected: `OK` (the navbar uses `[[[ ... ]]]` JS templating which is valid YAML strings — should parse).

If yaml fails: re-read the file around the edits, fix indentation/structure, re-run.

---

## Task 9: Edit `configuration.yaml`

**Files:**
- Modify: `homeassistant/config/configuration.yaml`

- [ ] **Step 1: Add `homeassistant.packages` block at top of file**

Read current first lines:
```bash
head -3 /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/configuration.yaml
```
Expected first line: `# Loads default set of integrations. Do not remove.`

Edit the file to insert `homeassistant: packages:` block immediately above `default_config:`. The new top of the file should be:

```yaml
homeassistant:
  packages: !include_dir_named packages

# Loads default set of integrations. Do not remove.
default_config:
```

- [ ] **Step 2: Append `dashboard-hemma` entry under `lovelace.dashboards`**

Locate the existing `lovelace.dashboards:` block (around line 27–40). Append a third dashboard entry after `dashboard-test:`:

Old (last 5 lines of the block):
```yaml
    dashboard-test:
      mode: yaml
      filename: dashboards/dashboard_test.yaml
      title: All Devices
      icon: mdi:home-variant
      show_in_sidebar: true
```

New:
```yaml
    dashboard-test:
      mode: yaml
      filename: dashboards/dashboard_test.yaml
      title: All Devices
      icon: mdi:home-variant
      show_in_sidebar: true
    dashboard-hemma:
      mode: yaml
      filename: dashboards/hemma/hemma.yaml
      title: Hemma
      icon: mdi:home-heart
      show_in_sidebar: true
```

- [ ] **Step 3: Verify edits**

Run:
```bash
grep -n "homeassistant:\|packages: !include_dir_named\|dashboard-hemma:" /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/configuration.yaml
```
Expected: 3 lines — the `homeassistant:` block at top, the packages include, and the `dashboard-hemma:` entry.

- [ ] **Step 4: YAML lint configuration.yaml**

Run:
```bash
python3 -c "
import yaml
class Loader(yaml.SafeLoader):
    pass
def constructor(loader, node):
    return None
for tag in ['!include','!include_dir_merge_named','!include_dir_named']:
    Loader.add_constructor(tag, constructor)
yaml.load(open('/Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/configuration.yaml'),Loader=Loader)
print('OK')
"
```
Expected: `OK`. Custom HA `!include*` tags are stubbed so the parse succeeds.

---

## Task 10: Create empty `dashboards/hemma/hemma.yaml` skeleton

**Files:**
- Create: `homeassistant/config/dashboards/hemma/hemma.yaml`

Author the dashboard file in two steps: first the file shell with `views:` empty, then populate views one by one in Tasks 11–14. This keeps each commit reviewable.

- [ ] **Step 1: Create dir**

Run: `mkdir -p /Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/hemma`

- [ ] **Step 2: Write skeleton file**

Create `/Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/hemma/hemma.yaml` with content:

```yaml
# Hemma Dashboard — generated from spec docs/superpowers/specs/2026-05-09-hemma-dashboard-design.md
# Templates loaded from /config/dashboards/templates/button_cards/

button_card_templates: !include_dir_merge_named /config/dashboards/templates/button_cards

views: []
```

- [ ] **Step 3: Verify YAML**

Run:
```bash
python3 -c "
import yaml
class L(yaml.SafeLoader):
    pass
for t in ['!include','!include_dir_merge_named','!include_dir_named']:
    L.add_constructor(t, lambda l,n: None)
print(yaml.load(open('/Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/hemma/hemma.yaml'),Loader=L))
"
```
Expected: `{'button_card_templates': None, 'views': []}`

---

## Task 11: Author Home view

**Files:**
- Modify: `homeassistant/config/dashboards/hemma/hemma.yaml` (replace `views: []` with views list containing Home)

- [ ] **Step 1: Replace `views: []` with the full Home view**

Replace the line `views: []` with:

```yaml
views:
  # ------------------------------------------------------
  # HOME
  # ------------------------------------------------------
  - type: custom:grid-layout
    title: home
    path: home
    layout: !include /config/dashboards/templates/includes/hemma_screen_layout.yaml
    cards:
      # ROOM HERO CARD
      - type: custom:button-card
        template: hemma_room
        name: Home
        variables:
          image: home
          image_position: center center
          temp_unit: 'C'

          show_climate: false

          show_lights: true
          light_group_entity: light.all_lights
          light_entity_1: light.bedroom_lights
          light_entity_2: light.living_room_lights

          show_presence: true
          presence_entity_1: person.sergei_kharchikov

          show_weather: true
          weather_entity: weather.forecast_home

          show_media: true
          show_media_player_1: true
          media_player_1: media_player.xgimi_horizon_pro_2
          show_media_player_2: true
          media_player_2: media_player.office_speaker

      # MOBILE NAVBAR
      - !include /config/dashboards/templates/includes/hemma_navbar_mobile.yaml

      # ENTITY CARDS
      - type: custom:layout-card
        class: hemma-entities
        layout_type: custom:grid-layout
        layout: !include /config/dashboards/templates/includes/hemma_entity_layout.yaml
        cards:
          - type: custom:button-card
            template: hemma_thermostat
            entity: climate.zhimi_mc2a_818a_heater
            name: Heater
            variables:
              temp_sensor: sensor.zhimi_mc2a_818a_temperature

          - type: custom:button-card
            template: hemma_fan
            entity: fan.dmaker_1c_8495_fan
            name: Fan

          - type: custom:button-card
            template: hemma_vacuum
            entity: vacuum.xiaomi_b106eu_5513_robot_cleaner
            name: Vacuum
            variables:
              battery_entity: sensor.xiaomi_b106eu_5513_battery_level

          - type: custom:button-card
            template: hemma_network
            entity: sensor.vodafone_hg8247x6_8n_10_gateway_external_ip
            name: WAN

          - type: custom:button-card
            template: hemma_entity
            entity: sensor.system_monitor_processor_temperature
            name: CPU Temp
            variables:
              icon: temp-medium

          - type: custom:button-card
            template: hemma_entity
            entity: sensor.system_monitor_disk_free
            name: Disk Free
            variables:
              icon: electric
```

- [ ] **Step 2: YAML lint the updated dashboard**

Run:
```bash
python3 -c "
import yaml
class L(yaml.SafeLoader):
    pass
for t in ['!include','!include_dir_merge_named','!include_dir_named']:
    L.add_constructor(t, lambda l,n: None)
d=yaml.load(open('/Users/sergeikharchikov/dev/personal/pi-setup/homeassistant/config/dashboards/hemma/hemma.yaml'),Loader=L)
assert len(d['views']) == 1, f'expected 1 view, got {len(d[\"views\"])}'
print('OK')
"
```
Expected: `OK`

---

## Task 12: Author Bedroom view

**Files:**
- Modify: `homeassistant/config/dashboards/hemma/hemma.yaml` (append a second item to `views:`)

- [ ] **Step 1: Append Bedroom view directly after the Home view**

Add the following block as a sibling of the Home view block (same indent, inserted between Home view and the previous closing of `views:` list, OR appended at the end if no other items follow):

```yaml
  # ------------------------------------------------------
  # BEDROOM
  # ------------------------------------------------------
  - type: custom:grid-layout
    title: bedroom
    path: bedroom
    layout: !include /config/dashboards/templates/includes/hemma_screen_layout.yaml
    cards:
      # ROOM HERO CARD
      - type: custom:button-card
        template: hemma_room
        name: Bedroom
        variables:
          image: bedroom
          image_position: center center
          temp_unit: 'C'

          show_climate: true
          climate_entity_1: climate.zhimi_mc2a_818a_heater
          temp_sensor_1: sensor.zhimi_mc2a_818a_temperature

          show_lights: true
          light_group_entity: light.bedroom_lights
          light_entity_1: light.ewelink_ck_bl702_al_01_7009_z102lg03_1
          light_entity_2: light.ewelink_ck_bl702_al_01_7009_z102lg03_1_2
          light_entity_3: light.wifi_gu10
          light_entity_4: light.wifi_gu10_2

          show_presence: false
          show_media: false
          show_weather: false

      # MOBILE NAVBAR
      - !include /config/dashboards/templates/includes/hemma_navbar_mobile.yaml

      # ENTITY CARDS
      - type: custom:layout-card
        class: hemma-entities
        layout_type: custom:grid-layout
        layout: !include /config/dashboards/templates/includes/hemma_entity_layout.yaml
        cards:
          - type: custom:button-card
            template: hemma_light
            entity: light.bedroom_lights
            name: All Bedroom

          - type: custom:button-card
            template: hemma_light
            entity: light.ewelink_ck_bl702_al_01_7009_z102lg03_1
            name: GU10 1

          - type: custom:button-card
            template: hemma_light
            entity: light.ewelink_ck_bl702_al_01_7009_z102lg03_1_2
            name: GU10 2

          - type: custom:button-card
            template: hemma_light
            entity: light.wifi_gu10
            name: GU10 3

          - type: custom:button-card
            template: hemma_light
            entity: light.wifi_gu10_2
            name: GU10 4

          - type: custom:button-card
            template: hemma_thermostat
            entity: climate.zhimi_mc2a_818a_heater
            name: Heater
            variables:
              temp_sensor: sensor.zhimi_mc2a_818a_temperature

          - type: custom:button-card
            template: hemma_entity
            entity: sensor.smart_toothbrush_e773_battery
            name: Toothbrush Battery
            variables:
              icon: electric

          - type: custom:button-card
            template: hemma_entity
            entity: sensor.smart_toothbrush_e773_score
            name: Toothbrush Score

          - type: custom:button-card
            template: hemma_motion
            variables:
              default_name: Motion
              sensor_1: binary_sensor.tze200_3towulqd_ts0601_occupancy
              label_1: Bedroom
              sensor_2: binary_sensor.smart_toothbrush_e773_toothbrush
              label_2: Toothbrush
```

- [ ] **Step 2: YAML lint**

Run the same check as Task 11 step 2 but with `assert len(d['views']) == 2`.

Expected: `OK`

---

## Task 13: Author Living Room view

**Files:**
- Modify: `homeassistant/config/dashboards/hemma/hemma.yaml` (append third view)

- [ ] **Step 1: Append Living Room view after Bedroom view**

```yaml
  # ------------------------------------------------------
  # LIVING ROOM
  # ------------------------------------------------------
  - type: custom:grid-layout
    title: living-room
    path: living-room
    layout: !include /config/dashboards/templates/includes/hemma_screen_layout.yaml
    cards:
      # ROOM HERO CARD
      - type: custom:button-card
        template: hemma_room
        name: Living Room
        variables:
          image: livingroom
          image_position: center center
          temp_unit: 'C'

          show_climate: false

          show_lights: true
          light_group_entity: light.living_room_lights
          light_entity_1: light.wled
          light_entity_2: light.yeelink_monoa_488c_light

          show_presence: false
          show_weather: false

          show_media: true
          show_media_player_1: true
          media_player_1: media_player.xgimi_horizon_pro_2

      # MOBILE NAVBAR
      - !include /config/dashboards/templates/includes/hemma_navbar_mobile.yaml

      # ENTITY CARDS
      - type: custom:layout-card
        class: hemma-entities
        layout_type: custom:grid-layout
        layout: !include /config/dashboards/templates/includes/hemma_entity_layout.yaml
        cards:
          - type: custom:button-card
            template: hemma_light
            entity: light.living_room_lights
            name: All Living

          - type: custom:button-card
            template: hemma_light
            entity: light.wled
            name: WLED

          - type: custom:button-card
            template: hemma_light
            entity: light.yeelink_monoa_488c_light
            name: Ceiling

          - type: custom:button-card
            template: hemma_media
            entity: media_player.xgimi_horizon_pro_2
            name: Projector
            variables:
              icon: tv

          - type: custom:button-card
            template: hemma_fan
            entity: fan.dmaker_1c_8495_fan
            name: Fan

          - type: custom:button-card
            template: hemma_motion
            variables:
              default_name: Motion
              sensor_1: binary_sensor.human_presence_sensor_2
              label_1: Living Room
```

- [ ] **Step 2: YAML lint**

Same check as before with `assert len(d['views']) == 3`.

---

## Task 14: Author Office view

**Files:**
- Modify: `homeassistant/config/dashboards/hemma/hemma.yaml` (append fourth view)

- [ ] **Step 1: Append Office view after Living Room view**

```yaml
  # ------------------------------------------------------
  # OFFICE
  # ------------------------------------------------------
  - type: custom:grid-layout
    title: office
    path: office
    layout: !include /config/dashboards/templates/includes/hemma_screen_layout.yaml
    cards:
      # ROOM HERO CARD
      - type: custom:button-card
        template: hemma_room
        name: Office
        variables:
          image: livingroom    # placeholder until office.jpg ships
          image_position: center center
          temp_unit: 'C'

          show_climate: false
          show_lights: false
          show_presence: false
          show_weather: false

          show_media: true
          show_media_player_1: true
          media_player_1: media_player.office_speaker

      # MOBILE NAVBAR
      - !include /config/dashboards/templates/includes/hemma_navbar_mobile.yaml

      # ENTITY CARDS
      - type: custom:layout-card
        class: hemma-entities
        layout_type: custom:grid-layout
        layout: !include /config/dashboards/templates/includes/hemma_entity_layout.yaml
        cards:
          - type: custom:button-card
            template: hemma_media
            entity: media_player.office_speaker
            name: Speaker
            variables:
              icon: homepod

          - type: custom:button-card
            template: hemma_entity
            entity: sensor.hp_deskjet_2800_series_black_ink
            name: Black Ink
            variables:
              icon: decrease

          - type: custom:button-card
            template: hemma_entity
            entity: sensor.hp_deskjet_2800_series_tri_color_ink
            name: Color Ink

          - type: custom:button-card
            template: hemma_entity
            entity: sensor.system_monitor_processor_temperature
            name: CPU Temp
            variables:
              icon: temp-medium

          - type: custom:button-card
            template: hemma_entity
            entity: sensor.system_monitor_disk_free
            name: Disk Free
            variables:
              icon: electric

          - type: custom:button-card
            template: hemma_vacuum
            entity: vacuum.xiaomi_b106eu_5513_robot_cleaner
            name: Vacuum
            variables:
              battery_entity: sensor.xiaomi_b106eu_5513_battery_level

          - type: custom:button-card
            template: hemma_motion
            variables:
              default_name: Motion
              sensor_1: binary_sensor.door_sensor_white
              label_1: Office Door
```

- [ ] **Step 2: YAML lint, assert 4 views**

Same check as before with `assert len(d['views']) == 4`.

Expected: `OK`

---

## Task 15: Commit 2 — customisations + dashboard authoring

(Spec called for 3 commits; for review clarity we collapse helpers/navbar/config edits + dashboard authoring into a single commit because the dashboard depends on the navbar/helpers being correct.)

- [ ] **Step 1: Stage all modified + new files**

```bash
cd /Users/sergeikharchikov/dev/personal/pi-setup
git add homeassistant/config/configuration.yaml \
        homeassistant/config/packages/hemma_helpers.yaml \
        homeassistant/config/dashboards/templates/includes/hemma_navbar_mobile.yaml \
        homeassistant/config/dashboards/hemma/hemma.yaml
```

- [ ] **Step 2: Verify staged**

Run: `git diff --cached --stat`
Expected:
- `configuration.yaml` — small diff (+ a few lines)
- `hemma_helpers.yaml` — small diff (5 edits)
- `hemma_navbar_mobile.yaml` — moderate diff (kitchen → office, popups removed)
- `dashboards/hemma/hemma.yaml` — large new file (4 views)

- [ ] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
homeassistant: add Hemma dashboard with 4 views

- Customise hemma_helpers.yaml: motion sensor IDs override upstream
  defaults; thermostat target temp range switched to °C; default mode
  set to heat (Xiaomi heater doesn't cool).
- Customise hemma_navbar_mobile.yaml: kebab-case routes, Office added,
  Kitchen + Rooms popup + Scenes popup removed.
- Register dashboard-hemma in configuration.yaml; add packages include.
- Author dashboards/hemma/hemma.yaml with Home, Bedroom, Living Room,
  Office views mapped to user's existing entities.

Spec: docs/superpowers/specs/2026-05-09-hemma-dashboard-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: Verify commit**

Run: `git log --oneline -2`
Expected: latest two commits are the assets-copy commit and the new customisation commit.

---

## Task 16: Output user-facing manual-step checklist

**Files:** none (printed instructions for the user).

The spec calls for two manual user steps that cannot be automated. After implementation, print this exact checklist for the user to follow.

- [ ] **Step 1: Print the manual steps**

Print verbatim:

```
================================================================
HEMMA DASHBOARD — REQUIRED MANUAL STEPS
================================================================

1. Install HACS cards (HACS → Frontend → Explore & Download Repositories):
   - button-card                (RomRider/button-card)
   - lovelace-navbar-card       (joseluis9595/lovelace-navbar-card)
   - browser_mod                (thomasloven/hass-browser_mod)
   - lovelace-more-info-card    (thomasloven/lovelace-more-info-card)
   - lovelace-mushroom          (piitaya/lovelace-mushroom)
   - uix                        (Lint-Free-Technology/uix)
   - kiosk-mode                 (NemesisRE/kiosk-mode)  [optional]

   ⚠ Do NOT install layout-card via HACS. Hemma ships a modified build
   under /local/layout-card-modified/.

2. Restart Home Assistant after HACS installs.

3. Add 10 Lovelace resources via UI
   (Settings → Dashboards → Resources → Add Resource).
   Add in this exact order — module type unless noted:

       /hacsfiles/button-card/button-card.js
       /local/layout-card-modified/layout-card-modified.js
       /hacsfiles/lovelace-navbar-card/navbar-card.js
       /local/navbar-popup-caret/navbar-popup-caret.js
       /local/navbar-sidebar-offset/navbar-sidebar-offset.js
       /hacsfiles/browser_mod/browser_mod.js
       /hacsfiles/lovelace-more-info-card/more-info-card.js
       /hacsfiles/lovelace-mushroom/mushroom.js
       /hacsfiles/uix/uix.js
       /local/hemma/fonts/hanken-grotesk.css        ← Stylesheet (CSS)

4. Restart Home Assistant.

5. Activate the Hemma theme:
   Settings → Profile → Themes → Hemma.

6. Open the new sidebar entry "Hemma".
   Smoke test:
   - Navigate to all 4 views via the navbar (Home → Bedroom → Living
     Room → Office). Each URL should be:
       /dashboard-hemma/{home,bedroom,living-room,office}
   - Hero badges render: lights, presence (Home only), weather
     (Home only), media (Home + Office + Living Room).
   - Tap a light tile → light toggles.
   - Tap thermostat tile → climate set to heat / off.
   - Verify HA logs (Settings → System → Logs) — no warnings about
     binary_sensor.living_room_hub_motion or hue_motion_sensor_motion
     (those upstream defaults were overridden in helpers).
================================================================
```

---

## Task 17: Smoke-test verification (run after the user completes manual steps)

**Files:** none.

This task is a verification gate. It is run AFTER the user has performed Task 16. Re-engage the executing agent to run these checks once the user reports manual steps are complete.

- [ ] **Step 1: HA Check Configuration**

Either via UI (Settings → System → Check Configuration) or, if `ha` CLI available:
```bash
ha core check
```
Expected: `Configuration is valid`.

- [ ] **Step 2: Verify Lovelace resources via API**

User must export a long-lived access token as `$HA_TOKEN` and supply HA host. Run:
```bash
curl -sH "Authorization: Bearer $HA_TOKEN" \
  http://<ha-host>:8123/api/lovelace/resources \
  | python3 -c "import sys, json; r=json.load(sys.stdin); print('\n'.join(sorted([x['url'] for x in r])))"
```
Expected: 10 URLs listed, matching the list in Task 16 step 3.

- [ ] **Step 3: Browser smoke test (manual)**

Open browser DevTools (F12) → Console tab. Navigate to `http://<ha-host>:8123/dashboard-hemma/home`. Confirm:
- No red console errors
- Network tab shows all 10 resources loading 200 OK
- Hanken Grotesk font is applied (visible in computed styles for body text)

- [ ] **Step 4: Navigation smoke test (manual)**

Tap each navbar entry. Confirm URL transitions:
- `/dashboard-hemma/home` → loads, weather badge shows
- `/dashboard-hemma/bedroom` → loads, climate badge shows heater state
- `/dashboard-hemma/living-room` → loads, media badge shows projector when active
- `/dashboard-hemma/office` → loads, speaker tile present

If any URL 404s, the navbar Task 8 edits weren't fully applied. Re-run the grep checks from Task 8 step 4 + step 8.

- [ ] **Step 5: Tap-action verification (manual)**

- Tap a light tile (e.g., GU10 1 in Bedroom view) → light toggles. If service errors in HA logs, the `script.hemma_light_smart_toggle` helper isn't loaded — re-verify Task 7 commit + HA restart.
- Tap the heater thermostat tile → state toggles between `off` and `heat`. If error `Service does not support hvac_mode 'cool'`, the helper override from Task 7 step 5 didn't apply — verify `input_select.hemma_thermostat_mode.state` is `heat` via Developer Tools → States.

- [ ] **Step 6: Mark complete**

Once all checks pass, the implementation is done. The original two dashboards (`Mobile`, `All Devices`) should still be present and unchanged in the sidebar.

---

## Self-Review Notes

- **Spec coverage:**
  - File layout (spec lines ~75–98) → Tasks 2–4
  - View 1 Home → Task 11
  - View 2 Bedroom → Task 12
  - View 3 Living Room → Task 13
  - View 4 Office → Task 14
  - Navbar customisation (spec section "Navbar customisation") → Task 8
  - Helpers initial values (spec section "Helpers initial values") → Task 7
  - Configuration changes (spec section) → Task 9
  - Lovelace resources + theme + HACS deps → Task 16 (manual)
  - Verification (spec section) → Task 17
  - Implementation phases (spec) → mapped to Tasks 5 (commit 1), 15 (commit 2 — collapsed helpers+config+dashboard into one for review-coherence)
- **Risks coverage:** All risk-table items either prevented by tasks (kebab path, helper overrides, resource order) or surfaced as smoke-test checks (Task 17 step 5).
- **Out-of-scope items** (custom office.jpg, AQI popup, doorbell/lock cards, kitchen view) intentionally not in any task.
