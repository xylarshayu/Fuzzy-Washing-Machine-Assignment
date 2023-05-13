# Fuzzy-Washing-Machine-Assignment
Basic college assignment for fuzzy washing machine.
By Ayush Wardhan 19103202

## Tables of Input & Output Variables

INPUT VARIABLE |  MEMBERSHIP VALUE |  MEMBERSHIP RANGE
---- | ---- | ----
dirtiness | ["small", "medium", "large"] | [0, 100]
typeof_dirt | ["not greasy", "medium", "greasy"] | [0, 100]
typeof_fabric | ["silk", "woolen", "cotton"] | [0, 100]
cloth_volume | ["small", "medium", "large"] | [0, 100]

OUTPUT VARIABLE |  MEMBERSHIP VALUE |  MEMBERSHIP RANGE
---- | ---- | ----
washing_time | ["very short", "short", "medium", "long", "very long"] | [0, 100]
washing_speed | ["very slow", "slow", "medium", "fast", "very fast"] | [0, 1200]
water_intake | ["little", "normal", "a lot"] | [0, 100]
water_temperature | ["low", "normal", "high"] | [0, 80]

## Rules of Inference

1. If (dirtiness is "small") and (typeof_dirt is "not greasy") and (typeof_fabric is "silk") and (cloth_volume is "small") then (washing_speed is "very slow")
2. If (dirtiness is "large") and (typeof_dirt is "greasy") and (typeof_fabric is "cotton") and (cloth_volume is Large ) then (washing_speed is "very fast")
3. If (dirtiness is "large") and (typeof_dirt is "not greasy") and (typeof_fabric is "woolen") and
(cloth_volume is "medium") then (washing_speed is "medium")
3. If (dirtiness is "large") and (typeof_dirt is "greasy") and (typeof_fabric is "cotton") and (cloth_volume is "large") then (washing_time is "very long", water_intake is "a lot", water_temperature is "high")
4. If (dirtiness is "medium") and (typeof_dirt is "medium") and (typeof_fabric is "woolen") and (cloth_volume is "medium") then (washing_time is "medium", water_intake is "normal", water_temperature is "normal")
5. If (dirtiness is "small") and (typeof_dirt is "not greasy") and (typeof_fabric is "silk") and (cloth_volume is "small") then (washing_time is "short", water_intake is "little", water_temperature is "low")

**Triangular Membership function to be assumed**

## Example

When the type of clothes is 21.5, type of dirty is 20.8, Dirtiness of Clothes is 50 and volume of clothes is 28, determine what is washing time, water intake, washing speed and water temperature.
