# Hemma Dashboard — Design Spec

**Date:** 2026-05-09
**Status:** Approved (pending user review of this spec)
**Owner:** Sergei Kharchikov

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
  - `dashboards/templates/` (button-card templates + includes)
  - `themes/hemma/hemma.yaml`
  - `packages/hemma_helpers.yaml`
  - `www/hemma/` (icons, fonts, room images, mobile bgs, weather icons)
  - `www/layout-card-modified/layout-card-modified.js`
  - `www/navbar-popup-caret/navbar-popup-caret.js`
  - `www/navbar-sidebar-offset/navbar-sidebar-offset.js`

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
│   └── templates/                           # NEW — copied verbatim
│       ├── button_cards/
│       │   ├── badges/   (10 files)
│       │   ├── base/     (8 files)
│       │   ├── cards/    (16 files)
│       │   └── popups/   (3 files)
│       └── includes/     (4 files)
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
- `show_climate: true`
  - `climate_entity_1: climate.zhimi_mc2a_818a_heater`
  - `temp_sensor_1: sensor.zhimi_mc2a_818a_temperature`
  - `temp_unit: 'C'`
- `show_lights: true`
  - `light_group_entity: light.all_lights`
  - `light_entity_1: light.bedroom_lights`
  - `light_entity_2: light.living_room_lights`
- `show_presence: true`
  - `presence_entity_1: person.sergei_kharchikov`
- `show_weather: true`
  - `weather_entity: weather.forecast_home`
- `show_media: true`
  - `show_media_player_1: true`, `media_player_1: media_player.xgimi_horizon_pro_2`
  - `show_media_player_2: true`, `media_player_2: media_player.office_speaker`

**Mobile navbar** (`hemma_navbar_mobile`): 4 entries — Home, Bedroom, Living, Office.

**Entity grid**:
- `hemma_thermostat` → `climate.zhimi_mc2a_818a_heater` (variable `temp_sensor: sensor.zhimi_mc2a_818a_temperature`)
- `hemma_fan` → `fan.dmaker_1c_8495_fan`
- `hemma_vacuum` → `vacuum.xiaomi_b106eu_5513_robot_cleaner` (variable `battery_entity: sensor.xiaomi_b106eu_5513_battery_level`)
- `hemma_network` → `sensor.vodafone_hg8247x6_8n_10_gateway_external_ip`
- `hemma_default` tile → `sensor.system_monitor_processor_temperature` (icon: `temp-medium`)
- `hemma_default` tile → `sensor.system_monitor_disk_free` (icon: `electric` or generic)

### View 2: Bedroom (`path: bedroom`)

**Hero card**:
- `image: bedroom`
- `show_climate: true`, `climate_entity_1: climate.zhimi_mc2a_818a_heater`, `temp_sensor_1: sensor.zhimi_mc2a_818a_temperature`
- `show_lights: true`, `light_group_entity: light.bedroom_lights`, members `light.ewelink_*_1`, `light.ewelink_*_1_2`, `light.wifi_gu10`, `light.wifi_gu10_2`
- `show_presence: true`, `presence_entity_1: binary_sensor.tze200_3towulqd_ts0601_occupancy`

**Entity grid**:
- `hemma_light` → `light.bedroom_lights`
- `hemma_light` × 4 individual: `light.ewelink_ck_bl702_al_01_7009_z102lg03_1`, `_1_2`, `light.wifi_gu10`, `light.wifi_gu10_2`
- `hemma_thermostat` → `climate.zhimi_mc2a_818a_heater`
- `hemma_default` → `sensor.smart_toothbrush_e773_battery` (icon: `electric`)
- `hemma_default` → `sensor.smart_toothbrush_e773_score`
- `hemma_motion` → `binary_sensor.smart_toothbrush_e773_toothbrush`
- `hemma_motion` → `binary_sensor.tze200_3towulqd_ts0601_occupancy`

### View 3: Living Room (`path: livingroom`)

**Hero card**:
- `image: livingroom`
- `show_lights: true`, `light_group_entity: light.living_room_lights`, members `light.wled`, `light.yeelink_monoa_488c_light`
- `show_presence: true`, `presence_entity_1: binary_sensor.human_presence_sensor_2`
- `show_media: true`, `media_player_1: media_player.xgimi_horizon_pro_2`

**Entity grid**:
- `hemma_light` → `light.living_room_lights`
- `hemma_light` → `light.wled`
- `hemma_light` → `light.yeelink_monoa_488c_light`
- `hemma_media` → `media_player.xgimi_horizon_pro_2`
- `hemma_fan` → `fan.dmaker_1c_8495_fan`
- `hemma_motion` → `binary_sensor.human_presence_sensor_2`

### View 4: Office (`path: office`)

**Hero card**:
- `image: livingroom` (placeholder — replace with `office.jpg` later)
- `show_presence: true`, `presence_entity_1: binary_sensor.door_sensor_white`
- `show_media: true`, `media_player_1: media_player.office_speaker`

**Entity grid**:
- `hemma_media` → `media_player.office_speaker`
- `hemma_default` → `sensor.hp_deskjet_2800_series_black_ink` (icon: `decrease`)
- `hemma_default` → `sensor.hp_deskjet_2800_series_tri_color_ink`
- `hemma_default` → `sensor.system_monitor_processor_temperature`
- `hemma_default` → `sensor.system_monitor_disk_free`
- `hemma_motion` → `binary_sensor.door_sensor_white`
- `hemma_vacuum` → `vacuum.xiaomi_b106eu_5513_robot_cleaner`

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

Single PR with these ordered phases (each verifiable independently):

1. **Copy Hemma assets** — `templates/`, `themes/hemma/`, `packages/hemma_helpers.yaml`, `www/hemma/`, `www/layout-card-modified/`, `www/navbar-popup-caret/`, `www/navbar-sidebar-offset/` into `homeassistant/config/`.
2. **`configuration.yaml` edits** — add packages include, register dashboard.
3. **Author `dashboards/hemma/hemma.yaml`** — 4 views mapped to user entities (per View design above).
4. **User-side manual steps** — install HACS cards, add Lovelace resources, enable Hemma theme.
5. **Smoke test** — restart HA, open `Hemma` dashboard, verify each view loads + badges render.

## Verification

- HA Check Configuration tool returns no errors after step 2 + 3
- `curl /api/lovelace/resources` lists all 10 resources
- All 4 views accessible from sidebar Hemma entry
- Hero cards render badges for climate/lights/presence/weather/media on Home view
- Mobile navbar links navigate between views
- Light tap toggles the light; thermostat tap opens climate popup

## Risks & mitigations

| Risk | Mitigation |
|---|---|
| Climate badge expects HVAC, user has heater only | Heater is HA `climate` domain — should work. If badge misrenders, drop `show_climate` in Home/Bedroom hero and use `hemma_thermostat` card in entity grid only |
| Storage-mode Lovelace can't auto-load resources | Spec lists exact 10 URLs + verification curl. User adds via UI |
| Office view has no shipped image | Reuse `livingroom.jpg` initially; user drops `office.jpg` into `www/hemma/rooms/` later (no code change needed beyond `image: office`) |
| Modified `layout-card` collides with HACS-installed `layout-card` | README warns explicitly. Spec instructs not to install via HACS |
| Resource load order | Modules listed in order matching Hemma example. If navbar fails, swap navbar-card before navbar-* helpers |
| Theme name collision | Existing `themes/ios-dark-mode/` unaffected — Hemma adds new dir |
| Big diff (~50 files) makes review hard | Phase commits: (1) assets copy, (2) config edits, (3) hemma.yaml authoring |

## Out of scope (future work)

- Custom `office.jpg` artwork
- Additional rooms (kitchen, bathroom)
- Air quality popup (requires PM2.5/PM10/VOC/CO2 sensors not yet present)
- Doorbell / lock cards (no entities)
- Migrating existing Mobile/All Devices dashboards onto Hemma
