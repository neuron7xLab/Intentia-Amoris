from intentia_amoris.kernel.omega_economic_value import default_2026_valuation, usd_to_uah

v = default_2026_valuation()
print("Intentia Amoris v5 — 2026 Valuation")
print("replacement_private_usd:", v["replacement_cost_private_usd"])
print("replacement_private_uah:", usd_to_uah(v["replacement_cost_private_usd"], v["uah_rate"]))
print("replacement_production_usd:", v["replacement_cost_production_usd"])
print("replacement_production_uah:", usd_to_uah(v["replacement_cost_production_usd"], v["uah_rate"]))
print("omega_asset_score:", v["omega_asset_score"])
print("saas_scenarios_usd:", v["saas_scenarios_usd"])
