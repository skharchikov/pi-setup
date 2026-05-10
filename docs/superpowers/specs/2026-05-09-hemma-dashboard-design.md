# Hemma Dashboard — Design Spec

**Date:** 2026-05-09 (rev. 2026-05-10)
**Status:** Revised after meta-review — pending user re-approval
**Owner:** Sergei Kharchikov

## Changelog

- **2026-05-10:** Reviewer + meta-reviewer pass.
  - **Critical fix:** view paths kebab-cased (`livingroom` → `living-room`); navbar reframed as "copy + edit", not verbatim. Office route added; Kitchen + Rooms popup + Scenes popup removed from navbar.
  - **Important fix:** sensor tiles use `hemma_entity` (not `hemma_default`, which is base CSS only).
  - **Important fix:** `hemma_motion` consolidated to one card per room with `sensor_1..N` + `label_1..N` (template doesn't support per-sensor instancing).
  - **Important fix:** dropped `show_presence` on Bedroom/Living/Office hero cards (presence badge expects person-domain `home`/`away`; binary sensors always render "Away").
  - **Important fix:** dropped `show_climate` on Home hero (heater probe is bedroom-only, not whole-home).
  - **Important addition:** new "Helpers initial values" section covering `hemma_helpers.yaml` post-copy customisations (motion sensor IDs, °C target temp, heater hvac mode).
  - **Refuted by meta-review (no change):** `hemma_vacuum` battery_entity works via `hemma_entity` inheritance; climate badge `hvac_action` requirement has fallback that handles heaters; image dark variants ship for all rooms.
  - **Doc fix:** architecture diagram `base/` file count corrected (8 → 9).

## Goal

Add a third Home Assistant Lovelace dashboard inspired by [willsanderson/Hemma](https://github.com/willsanderson/Hemma) to `pi-setup/homeassistant/config/`. Existing `Mobile` (`test_default.yaml`) and `All Devices` (`dashboard_test.yaml`) dashboards remain untouched.

The new dashboard adopts Hemma's full template/theme/asset layout and exposes four views (Home, Bedroom, Living Room, Office) mapped to the entities currently used in the existing dashboards.

## Non-goals

- Replacing or migrating existing dashboards
- Refactoring `automations.yaml`, `scripts.yaml`, etc.
- Authoring custom Hemma templates beyond what the upstream repo provides
- Designing custom artwork — using Hemma's shipped `home.jpg`, `bedroom.jpg`, `livingroom.jpg`. Office reuses `livingroom.jpg` as placeholder

## Inputs

### Reference repo

- Source: `https://github.com/willsanderson/Hemma` (default branch `main`)
- Local clone for read-only inspection: `/tmp/Hemma`
- Files copied verbatim into pi-setup (no upstream modification):
  - `dashboards/templates/button_cards/` (button-card templates — base, badges, cards, popups)
  - `dashboards/templates/includes/hemma_screen_layout.yaml`
  - `dashboards/templates/includes/hemma_entity_layout.yaml`
  - `dashboards/templates/includes/hemma_navigation.yaml`
  - `themes/hemma/hemma.yaml`
  - `www/hemma/` (icons, fonts, room images, mobile bgs, weather icons)
  - `www/layout-card-modified/layout-card-modified.js`
  - `www/navbar-popup-caret/navbar-popup-caret.js`
  - `www/navbar-sidebar-offset/navbar-sidebar-offset.js`
- Files copied **and edited** (require user-specific customisation):
  - `dashboards/templates/includes/hemma_navbar_mobile.yaml` — routes hardcoded as `/dashboard-hemma/<path>`. Must drop Kitchen, Rooms popup, Scenes popup; add Office; ensure all 4 routes match the view `path:` values declared in `hemma.yaml`.
  - `packages/hemma_helpers.yaml` — `input_text.hemma_motion_*` defaults reference upstream-only sensor IDs (`binary_sensor.living_room_hub_motion`, `_hue_motion_sensor_motion`); replace with user's binary sensors. `input_number.hemma_thermostat_target_temperature` ships in °F (68–75); swap to °C (15–30). `input_select.hemma_thermostat_mode.initial` defaults to `cool`; switch to `heat` (heater doesn't cool). See "Helpers initial values" section below for full list.

### User entities

Discovered from `homeassistant/config/dashboards/*.yaml`.

| Domain | Entity | Notes |
|---|---|---|
| light | `light.all_lights` | Whole-home group |
| light | `light.bedroom_lights` | Bedroom group (members: 2× ewelink ck_bl702, 2× wifi_gu10) |
| light | `light.living_room_lights` | Living room group (members: wled, yeelink_monoa_488c) |
| light | `light.ewelink_ck_bl702_al_01_7009_z102lg03_1`, `_2` | Bedroom GU10s |
| light | `light.wifi_gu10`, `light.wifi_gu10_2` | Bedroom GU10s |
| light | `light.wled` | Living room WLED strip |
| light | `light.yeelink_monoa_488c_light` | Living room ceiling |
| climate | `climate.zhimi_mc2a_818a_heater` | Xiaomi heater (bedroom) |
| fan | `fan.dmaker_1c_8495_fan` | Living room fan |
| sensor | `sensor.zhimi_mc2a_818a_temperature` | Heater temp probe |
| sensor | `sensor.smart_toothbrush_e773_battery`, `_score` | Bathroom-adjacent (placed in Bedroom view) |
| sensor | `sensor.hp_deskjet_2800_series_black_ink`, `_tri_color_ink` | Office printer |
| sensor | `sensor.system_monitor_disk_free`, `_processor_temperature` | Pi system |
| sensor | `sensor.xiaomi_b106eu_5513_battery_level` | Vacuum battery |
| sensor | `sensor.vodafone_hg8247x6_8n_10_gateway_external_ip` | Network |
| binary_sensor | `binary_sensor.door_sensor_white` | Office door |
| binary_sensor | `binary_sensor.human_presence_sensor_2` | Living room |
| binary_sensor | `binary_sensor.tze200_3towulqd_ts0601_occupancy` | Bedroom |
| binary_sensor | `binary_sensor.smart_toothbrush_e773_toothbrush` | Bedroom |
| media_player | `media_player.xgimi_horizon_pro_2` | Living room projector |
| media_player | `media_player.office_speaker` | Office |
| vacuum | `vacuum.xiaomi_b106eu_5513_robot_cleaner` | Whole home |
| weather | `weather.forecast_home` | Outdoor weather |
| person | `person.sergei_kharchikov` | Presence |

## Architecture

```
pi-setup/homeassistant/config/
├── configuration.yaml                       # MODIFIED: +packages include, +dashboard-hemma entry
├── dashboards/
│   ├── dashboard_test.yaml                  # unchanged
│   ├── map.yaml                             # unchanged
│   ├── test_default.yaml                    # unchanged
│   ├── hemma/
│   │   └── hemma.yaml                       # NEW — 4 views, user-entity-mapped
│   └── templates/                           # NEW — copied (navbar EDITED, see below)
│       ├── button_cards/
│       │   ├── badges/   (10 files, verbatim)
│       │   ├── base/     (9 files, verbatim)
│       │   ├── cards/    (16 files, verbatim)
│       │   └── popups/   (3 files, verbatim)
│       └── includes/
│           ├── hemma_screen_layout.yaml     # verbatim
│           ├── hemma_entity_layout.yaml     # verbatim
│           ├── hemma_navigation.yaml        # verbatim
│           └── hemma_navbar_mobile.yaml     # EDITED (routes match user's view paths)
├── packages/
│   └── hemma_helpers.yaml                   # NEW
├── themes/
│   ├── ios-dark-mode/                       # unchanged
│   └── hemma/
│       └── hemma.yaml                       # NEW
└── www/
    ├── hemma/                               # NEW — fonts, icons, mobile/, rooms/, weather/
    ├── layout-card-modified/
    │   └── layout-card-modified.js          # NEW
    ├── navbar-popup-caret/
    │   └── navbar-popup-caret.js            # NEW
    └── navbar-sidebar-offset/
        └── navbar-sidebar-offset.js         # NEW
```

## View design

### View 1: Home (`path: home`)

**Hero card** (`hemma_room` template):
- `image: home`, `image_position: center center`
- `temp_unit: 'C'`
- `show_climate: false` — heater probe is bedroom-only, not whole-home. Climate badge moved to Bedroom view only.
- `show_lights: true`
  - `light_group_entity: light.all_lights`
  - `light_entity_1: light.bedroom_lights`
  - `light_entity_2: light.living_room_lights`
- `show_presence: true`
  - `presence_entity_1: person.sergei_kharchikov` *(person domain → renders correctly)*
- `show_weather: true`
  - `weather_entity: weather.forecast_home`
- `show_media: true`
  - `show_media_player_1: true`, `media_player_1: media_player.xgimi_horizon_pro_2`
  - `show_media_player_2: true`, `media_player_2: media_player.office_speaker`

**Mobile navbar** (edited `hemma_navbar_mobile.yaml` include): 4 entries — Home, Bedroom, Living Room, Office. URLs are `/dashboard-hemma/home`, `/bedroom`, `/living-room`, `/office`.

**Entity grid**:
- `hemma_thermostat` → `climate.zhimi_mc2a_818a_heater` (variable `temp_sensor: sensor.zhimi_mc2a_818a_temperature`)
- `hemma_fan` → `fan.dmaker_1c_8495_fan`
- `hemma_vacuum` → `vacuum.xiaomi_b106eu_5513_robot_cleaner` (variable `battery_entity: sensor.xiaomi_b106eu_5513_battery_level` — works via `hemma_entity` inheritance)
- `hemma_network` → `sensor.vodafone_hg8247x6_8n_10_gateway_external_ip`
- `hemma_entity` → `sensor.system_monitor_processor_temperature` (variables: `icon: temp-medium`)
- `hemma_entity` → `sensor.system_monitor_disk_free` (variables: `icon: electric`)

### View 2: Bedroom (`path: bedroom`)

**Hero card**:
- `image: bedroom`
- `temp_unit: 'C'`
- `show_climate: true`, `climate_entity_1: climate.zhimi_mc2a_818a_heater`, `temp_sensor_1: sensor.zhimi_mc2a_818a_temperature`
- `show_lights: true`, `light_group_entity: light.bedroom_lights`, members `light_entity_1: light.ewelink_ck_bl702_al_01_7009_z102lg03_1`, `light_entity_2: light.ewelink_ck_bl702_al_01_7009_z102lg03_1_2`, `light_entity_3: light.wifi_gu10`, `light_entity_4: light.wifi_gu10_2`
- `show_presence: false` — bedroom occupancy is binary_sensor; presence badge expects person-domain `home`/`away`. Surfaced in entity grid via `hemma_motion` instead.

**Entity grid**:
- `hemma_light` → `light.bedroom_lights`
- `hemma_light` × 4 individual: `light.ewelink_ck_bl702_al_01_7009_z102lg03_1`, `_1_2`, `light.wifi_gu10`, `light.wifi_gu10_2`
- `hemma_thermostat` → `climate.zhimi_mc2a_818a_heater` (variable `temp_sensor: sensor.zhimi_mc2a_818a_temperature`)
- `hemma_entity` → `sensor.smart_toothbrush_e773_battery` (variables: `icon: electric`)
- `hemma_entity` → `sensor.smart_toothbrush_e773_score`
- `hemma_motion` (single card) — variables:
  - `default_name: Motion`
  - `sensor_1: binary_sensor.tze200_3towulqd_ts0601_occupancy`, `label_1: Bedroom`
  - `sensor_2: binary_sensor.smart_toothbrush_e773_toothbrush`, `label_2: Toothbrush`

### View 3: Living Room (`path: living-room`)

> Note: kebab-case `living-room` matches navbar route `/dashboard-hemma/living-room`.

**Hero card**:
- `image: livingroom`
- `temp_unit: 'C'`
- `show_lights: true`, `light_group_entity: light.living_room_lights`, `light_entity_1: light.wled`, `light_entity_2: light.yeelink_monoa_488c_light`
- `show_presence: false` — `binary_sensor.human_presence_sensor_2` is `on`/`off`, not person-domain. Surfaced in entity grid via `hemma_motion`.
- `show_media: true`, `show_media_player_1: true`, `media_player_1: media_player.xgimi_horizon_pro_2`

**Entity grid**:
- `hemma_light` → `light.living_room_lights`
- `hemma_light` → `light.wled`
- `hemma_light` → `light.yeelink_monoa_488c_light`
- `hemma_media` → `media_player.xgimi_horizon_pro_2` (variables: `icon: tv`)
- `hemma_fan` → `fan.dmaker_1c_8495_fan`
- `hemma_motion` (single card) — variables:
  - `default_name: Motion`
  - `sensor_1: binary_sensor.human_presence_sensor_2`, `label_1: Living Room`

### View 4: Office (`path: office`)

**Hero card**:
- `image: livingroom` (placeholder — replace with `office.jpg` later)
- `temp_unit: 'C'`
- `show_presence: false` — `binary_sensor.door_sensor_white` is door state, not person presence. Surfaced via `hemma_motion`.
- `show_media: true`, `show_media_player_1: true`, `media_player_1: media_player.office_speaker`

**Entity grid**:
- `hemma_media` → `media_player.office_speaker` (variables: `icon: homepod`)
- `hemma_entity` → `sensor.hp_deskjet_2800_series_black_ink` (variables: `icon: decrease`)
- `hemma_entity` → `sensor.hp_deskjet_2800_series_tri_color_ink`
- `hemma_entity` → `sensor.system_monitor_processor_temperature` (variables: `icon: temp-medium`)
- `hemma_entity` → `sensor.system_monitor_disk_free` (variables: `icon: electric`)
- `hemma_vacuum` → `vacuum.xiaomi_b106eu_5513_robot_cleaner` (variables: `battery_entity: sensor.xiaomi_b106eu_5513_battery_level`)
- `hemma_motion` (single card) — variables:
  - `default_name: Motion`
  - `sensor_1: binary_sensor.door_sensor_white`, `label_1: Office Door`

## Navbar customisation

`dashboards/templates/includes/hemma_navbar_mobile.yaml` ships with hardcoded routes for Home, Living Room, Bedroom, Kitchen, plus a Rooms popup and a Scenes popup. User-specific edits required after copy:

- Replace all `/dashboard-hemma/kitchen` references → remove (no Kitchen view)
- Add `/dashboard-hemma/office` entries to the desktop top-nav, tablet nav, and phone-portrait nav (mirroring the structure of the Living Room entry)
- Remove the Rooms popup template usages (Bedroom + Kitchen + Living Room dropdown) — replace with direct flat links since we have only 4 rooms
- Remove the Scenes popup template usages (no scenes defined yet)
- Confirm every `url:` ends with one of: `/dashboard-hemma/home`, `/dashboard-hemma/bedroom`, `/dashboard-hemma/living-room`, `/dashboard-hemma/office`

The motion-badge `input_text.hemma_motion_*` references in this file are configured via helpers (next section), not edits to the navbar itself.

## Helpers initial values

After copying `packages/hemma_helpers.yaml`, edit it to match user's setup. Upstream defaults reference entities that don't exist in this HA install.

| Helper | Upstream default | Required value |
|---|---|---|
| `input_text.hemma_motion_living_room.initial` | `binary_sensor.living_room_hub_motion` | `binary_sensor.human_presence_sensor_2` |
| `input_text.hemma_motion_bedroom.initial` | `binary_sensor.hue_motion_sensor_motion` | `binary_sensor.tze200_3towulqd_ts0601_occupancy` |
| `input_text.hemma_motion_kitchen.initial` | `""` | leave blank (no Kitchen view) |
| `input_number.hemma_thermostat_target_temperature.min` | `68` (°F) | `15` (°C) |
| `input_number.hemma_thermostat_target_temperature.max` | `75` (°F) | `30` (°C) |
| `input_number.hemma_thermostat_target_temperature.unit_of_measurement` | `°F` | `°C` |
| `input_select.hemma_thermostat_mode.initial` | `cool` | `heat` (heater doesn't cool) |

Helpers also ship two ornamental template sensors that read `sensor.temperature` / `sensor.humidity` (don't exist in this install). They will resolve to `unavailable` — non-fatal, but adds startup warnings. Out of scope to fix; can be deleted later if noisy.

`script.hemma_light_smart_toggle` ships in helpers and is used by every `hemma_light` card. No customisation needed — works as-is.

## Configuration changes

### `homeassistant/config/configuration.yaml`

Add to top of `homeassistant:` section (create section if absent):

```yaml
homeassistant:
  packages: !include_dir_named packages
```

Append to existing `lovelace.dashboards:`:

```yaml
    dashboard-hemma:
      mode: yaml
      filename: dashboards/hemma/hemma.yaml
      title: Hemma
      icon: mdi:home-heart
      show_in_sidebar: true
```

Existing `test-default` and `dashboard-test` entries unchanged.

### Lovelace resources (manual via HA UI)

Settings → Dashboards → Resources → Add Resource (one per line, all `JavaScript Module` unless noted):

```
/hacsfiles/button-card/button-card.js
/hacsfiles/lovelace-navbar-card/navbar-card.js
/hacsfiles/browser_mod/browser_mod.js
/hacsfiles/lovelace-more-info-card/more-info-card.js
/hacsfiles/lovelace-mushroom/mushroom.js
/hacsfiles/uix/uix.js
/local/layout-card-modified/layout-card-modified.js
/local/navbar-popup-caret/navbar-popup-caret.js
/local/navbar-sidebar-offset/navbar-sidebar-offset.js
/local/hemma/fonts/hanken-grotesk.css   (Stylesheet)
```

Verify after install:

```bash
curl -sH "Authorization: Bearer $HA_TOKEN" http://<ha-host>:8123/api/lovelace/resources | jq
```

### Theme activation (manual)

Settings → Profile → Themes → Hemma.

### HACS deps (manual install via HACS UI)

- button-card (RomRider)
- lovelace-navbar-card (joseluis9595)
- browser_mod (thomasloven)
- lovelace-more-info-card (thomasloven)
- lovelace-mushroom (piitaya)
- uix (Lint-Free-Technology)
- kiosk-mode (NemesisRE) — optional

> ⚠ Do NOT install `layout-card` via HACS. Hemma ships a modified build under `/local/layout-card-modified/`.

## Implementation phases

Single PR, 3 commits + 2 manual user steps. Each commit verifiable on its own.

1. **Commit 1 — Copy Hemma assets (verbatim parts)**: copy `dashboards/templates/button_cards/`, verbatim `includes/` files, `themes/hemma/`, `www/hemma/`, `www/layout-card-modified/`, `www/navbar-popup-caret/`, `www/navbar-sidebar-offset/` into `homeassistant/config/`. Copy `packages/hemma_helpers.yaml` (will be edited in commit 2).
2. **Commit 2 — Customise helpers + navbar + register dashboard**: edit `packages/hemma_helpers.yaml` per "Helpers initial values" table; copy + edit `dashboards/templates/includes/hemma_navbar_mobile.yaml` per "Navbar customisation"; add `homeassistant.packages: !include_dir_named packages` to `configuration.yaml`; add `dashboard-hemma` entry under `lovelace.dashboards`. **Order matters**: `packages/` directory must exist (commit 1) before `!include_dir_named` runs.
3. **Commit 3 — Author `dashboards/hemma/hemma.yaml`**: 4 views (Home, Bedroom, Living Room, Office) per View design above.
4. **Manual step A** (user): install HACS cards (`button-card`, `lovelace-navbar-card`, `browser_mod`, `more-info-card`, `lovelace-mushroom`, `uix`, optional `kiosk-mode`).
5. **Manual step B** (user): add 10 Lovelace resources via UI (Settings → Dashboards → Resources). Enable Hemma theme (Settings → Profile → Themes).
6. **Smoke test**: restart HA. Open `Hemma` from sidebar. Tap each navbar entry — confirm URL is `/dashboard-hemma/{home,bedroom,living-room,office}` and view renders.

## Verification

After commit 2:
- `ha core check` (or HA UI Settings → System → Check Configuration) reports no errors

After commit 3:
- HA Check Configuration still passes
- Browser opens `/dashboard-hemma/home` without console errors (DevTools → Console)
- Network tab shows `hanken-grotesk.css` + all 9 JS resources loading 200 OK
- Each navbar tap navigates without 404 (route paths kebab-cased to match navbar)
- Bedroom hero climate badge animates when heater state ∈ {`heat`, `auto`} (non-`off`)
- Light tile tap toggles light (calls `script.hemma_light_smart_toggle`)
- Thermostat tile tap calls `climate.set_hvac_mode` with `heat` (verify in HA logs no `Service does not support response` errors)
- `curl -sH "Authorization: Bearer $HA_TOKEN" http://<ha-host>:8123/api/lovelace/resources | jq '.[].url'` returns all 10 expected URLs
- HA logs show no warnings referencing `binary_sensor.living_room_hub_motion` or `_hue_motion_sensor_motion` (helpers correctly overridden)

## Risks & mitigations

| Risk | Mitigation |
|---|---|
| Climate badge fan-icon animation needs `hvac_action` attr | Verified upstream fallback: badge animates whenever `state ∉ {off, unavailable, unknown}`. Heater state `heat` triggers animation regardless of `hvac_action`. No mitigation needed |
| Thermostat hardcoded `cool` fallback in `toggle_service_data` | `input_select.hemma_thermostat_mode.initial: heat` set in helpers (see Helpers initial values). Fallback only fires if input_select unavailable |
| Storage-mode Lovelace can't auto-load resources | Spec lists exact 10 URLs + verification curl. User adds via UI |
| Office view has no shipped image | Reuse `livingroom.jpg` initially; user drops `office.jpg` into `www/hemma/rooms/` later (only `image: office` swap needed in hemma.yaml) |
| Modified `layout-card` collides with HACS-installed `layout-card` | README warns explicitly. Spec instructs not to install via HACS |
| Resource load order | Order: button-card → layout-card-modified → navbar-card → navbar-popup-caret → navbar-sidebar-offset → browser_mod → more-info-card → mushroom → uix → hanken-grotesk.css. Modules before stylesheets, foundations before helpers |
| Theme name collision | Existing `themes/ios-dark-mode/` unaffected — Hemma adds new dir |
| Big diff (~50 files) makes review hard | 3 commits: (1) verbatim assets, (2) helpers + navbar edits + config, (3) dashboard authoring |
| Helper template sensors `Temp Color`/`Humidity Color` reference non-existent `sensor.temperature`/`sensor.humidity` | Cosmetic — sensors render `unavailable` but don't break dashboard. Out of scope to fix |
| HVAC tap calls `climate.set_hvac_mode` with unsupported mode if heater rejects `heat` | Verify with single tap during smoke test. If service errors, override `toggle_service_data` per-instance in `hemma.yaml` (force `heat`/`off` only) |

## Template variable matrix

Verified against `/tmp/Hemma/dashboards/templates/button_cards/{cards,base}/<template>.yaml` `variables:` blocks.

| Card template | Required `entity:` | `variables:` keys used | Source-of-truth file |
|---|---|---|---|
| `hemma_room` | — (hero card) | `image`, `image_position`, `temp_unit`, `show_climate`, `climate_entity_1..3`, `temp_sensor_1..5`, `humidity_sensor`, `quality_sensor`, `show_lights`, `light_group_entity`, `light_entity_1..4`, `show_presence`, `presence_entity_1..4`, `show_weather`, `weather_entity`, `weather_temp_sensor`, `show_media`, `show_media_player_1..4`, `media_player_1..4`, `pause_timeout_minutes` | `cards/hemma_room.yaml` |
| `hemma_thermostat` | `climate.*` | `temp_sensor` | `cards/hemma_thermostat.yaml` |
| `hemma_fan` | `fan.*` | `icon` (top-level button-card) | `cards/hemma_fan.yaml` |
| `hemma_vacuum` | `vacuum.*` | `battery_entity` (via `hemma_entity` inheritance), `icon` | `cards/hemma_vacuum.yaml`, `base/hemma_entity.yaml` |
| `hemma_network` | `sensor.*` (any) | (none — uses `entity` directly) | `cards/hemma_network.yaml` |
| `hemma_entity` | any | `icon`, `battery_entity`, plus `hemma_default` styling | `base/hemma_entity.yaml` |
| `hemma_light` | `light.*` | `show_toggle`, `toggle_service`, `toggle_service_data` (defaults call `script.hemma_light_smart_toggle`) | `cards/hemma_light.yaml` |
| `hemma_motion` | — (computed from `sensor_*`) | `default_name`, `sensor_1..6`, `label_1..6` | `cards/hemma_motion.yaml` |
| `hemma_media` | `media_player.*` | `icon` | `cards/hemma_media.yaml` |

> ⚠ `hemma_default` (in `base/`, not `cards/`) is CSS reset only — no entity rendering. Do NOT use as a sensor tile. Use `hemma_entity` instead.

## Out of scope (future work)

- Custom `office.jpg` artwork
- Additional rooms (kitchen, bathroom)
- Air quality popup (requires PM2.5/PM10/VOC/CO2 sensors not yet present)
- Doorbell / lock cards (no entities)
- Migrating existing Mobile/All Devices dashboards onto Hemma
