import json
import subprocess
import datetime
import sys
import os

def run_az_command(command):
    """Runs an Azure CLI command and returns the JSON output."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}", file=sys.stderr)
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from command '{command}'", file=sys.stderr)
        return []

def generate_content_json(output_path):
    """Generates content.json from Azure environment info."""
    
    print("Fetching Azure information...")
    
    # 1. Subscription Info
    sub_info = run_az_command("az account show")
    sub_name = sub_info.get("name", "Unknown")
    sub_id = sub_info.get("id", "Unknown")
    
    # 2. Resource Groups
    rgs = run_az_command("az group list")
    
    # 3. VNets
    vnets = run_az_command("az network vnet list")
    
    # 4. All Resources (summary)
    # Getting all resources might be heavy, so we'll do it per RG or just a summary count if too many
    # For now, let's get a list of all resources to summarize types
    all_resources = run_az_command("az resource list")
    
    slides = []
    
    # --- Slide 1: Title ---
    slides.append({
        "type": "title",
        "title": "Azure Environment Report",
        "subtitle": f"Subscription: {sub_name}\nID: {sub_id}\nDate: {datetime.date.today()}"
    })
    
    # --- Slide 2: Agenda ---
    slides.append({
        "type": "agenda",
        "title": "Agenda",
        "items": [
            "Executive Summary",
            "Network Topology",
            "Resource Group Details"
        ]
    })
    
    # --- Slide 3: Executive Summary ---
    resource_count = len(all_resources)
    rg_count = len(rgs)
    vnet_count = len(vnets)
    
    # Count resource types
    type_counts = {}
    for r in all_resources:
        rtype = r.get("type", "Unknown")
        type_counts[rtype] = type_counts.get(rtype, 0) + 1
    
    top_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_types_str = [f"{t[0]}: {t[1]}" for t in top_types]
    
    slides.append({
        "type": "content",
        "title": "Executive Summary",
        "items": [
            f"Subscription: {sub_name}",
            f"Total Resource Groups: {rg_count}",
            f"Total Resources: {resource_count}",
            f"Total VNets: {vnet_count}",
            "Top Resource Types:"
        ] + top_types_str,
        "notes": f"Overview of the Azure environment for subscription {sub_name}."
    })
    
    # --- Section: Network ---
    slides.append({
        "type": "section",
        "title": "Network Topology",
        "subtitle": "Virtual Networks and Subnets"
    })
    
    if not vnets:
        slides.append({
            "type": "content",
            "title": "Virtual Networks",
            "items": ["No Virtual Networks found in this subscription."]
        })
    else:
        for vnet in vnets:
            vnet_name = vnet.get("name")
            address_space = vnet.get("addressSpace", {}).get("addressPrefixes", [])
            subnets = vnet.get("subnets", [])
            location = vnet.get("location")
            
            subnet_items = []
            for s in subnets:
                prefix = s.get("addressPrefix", "N/A")
                subnet_items.append(f"- {s.get('name')}: {prefix}")
            
            slides.append({
                "type": "content",
                "title": f"VNet: {vnet_name}",
                "items": [
                    f"Location: {location}",
                    f"Address Space: {', '.join(address_space)}",
                    "Subnets:"
                ] + subnet_items,
                "notes": f"Details for Virtual Network {vnet_name}."
            })

    # --- Section: Resource Groups ---
    slides.append({
        "type": "section",
        "title": "Resource Group Details",
        "subtitle": "Resources by Group"
    })
    
    for rg in rgs:
        rg_name = rg.get("name")
        location = rg.get("location")
        
        # Filter resources for this RG
        rg_resources = [r for r in all_resources if r.get("resourceGroup") == rg_name]
        
        if not rg_resources:
            continue
            
        # Summarize resources in this RG
        rg_items = []
        for r in rg_resources[:8]: # Limit to 8 items to avoid overflow
            r_name = r.get("name")
            r_type = r.get("type").split('/')[-1] # Shorten type name
            rg_items.append(f"{r_name} ({r_type})")
            
        if len(rg_resources) > 8:
            rg_items.append(f"... and {len(rg_resources) - 8} more resources")
            
        slides.append({
            "type": "content",
            "title": f"RG: {rg_name}",
            "items": [f"Location: {location}", "Resources:"] + rg_items,
            "notes": f"Resources in {rg_name}."
        })

    # --- Slide: Summary ---
    slides.append({
        "type": "summary",
        "title": "Summary",
        "items": [
            "Azure environment visualization complete.",
            "Please review the resource distribution and network settings.",
            "Check the Azure Portal for more details."
        ]
    })

    # Output JSON
    content = {"slides": slides}
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated content JSON at {output_path}")
    print(f"Total slides: {len(slides)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = "output_manifest/azure_environment_content.json"
        
    generate_content_json(output_file)
