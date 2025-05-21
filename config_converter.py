# This script actually part of wg-custom repository (https://github.com/alex-dv9/database.git)
# --- Please keep in mind that I'M NOT CODER AT ALL so I have all rights to write bad code :) ---

import configparser, re
from io import StringIO

def configExtractor():

  # --- Extract all lines from given WireGuard configuration file

  wireguard_config_path = str(input("Please type full path to WireGuard .conf file below:\n--- "))
  
  with open(wireguard_config_path, "r") as f:
    wireguard_config_text = f.read()

  return wireguard_config_text

def configRefactor(config_text):

  # --- Refactor given WireGuard configuration file's text

  refactored_config_lines_array = []

  for line in config_text.strip().splitlines():
    refactored_line = line.strip()

    if not refactored_line or refactored_line.startswith("#"):
      continue

    line = re.sub(r"\s*#.*$", "", refactored_line).strip()
    refactored_config_lines_array.append(refactored_line)
    
  refactored_config_text = "\n".join(refactored_config_lines_array)

  return refactored_config_text

def configParser(refactored_config_text):

  # --- Parse refactored WireGuard configuration file text

  parser = configparser.ConfigParser(allow_no_value=False, strict=False, delimiters=("="))
  parser.read_file(StringIO(refactored_config_text))

  parsing_result = {}

  if "Interface" in parser:
    parsing_result["PrivateKey"] = parser["Interface"].get("PrivateKey")
    parsing_result["Address"] = parser["Interface"].get("Address")
    parsing_result["DNS"] = parser["Interface"].get("DNS")

  if "Peer" in parser:
    parsing_result["PublicKey"] = parser["Peer"].get("PublicKey")

    endpoint_scratch = parser["Peer"].get("Endpoint")

    if endpoint_scratch:
      m = re.match(r"([^:]+):(\d+)", endpoint_scratch)

      if m:
        parsing_result["EndpointAddress"] = m.group(1)
        parsing_result["EndpointPort"] = m.group(2)

  return parsing_result

def configCreator(parsed_config):

  # --- Finally, after all these functions iterations, we are creating wg-custom compatible configuration file

  print("!!! Configuration file will be stored in current directory")
  
  wgcustom_config_location = "config_template"

  with open(wgcustom_config_location, "w") as f:
    
    f.write(f"CONFIG_PRIVATEKEY='{parsed_config["PrivateKey"]}'\n")
    f.write(f"CONFIG_PUBLICKEY='{parsed_config["PublicKey"]}'\n")
    f.write(f"CONFIG_PEERADDRESS='{parsed_config["Address"]}'\n")
    f.write(f"CONFIG_ENDPOINTIP='{parsed_config["EndpointAddress"]}'\n")
    f.write(f"CONFIG_DNSSERVER='{parsed_config["DNS"]}'")

  print("!!! Configuration file was successfully generated !!!")

  return 0 

def main():
  
  # Extract lines from provided WireGuard configuration file
  wireguard_config_text = configExtractor()
  
  # Refactor extracted lines to configparser python module format
  refactored_config_text = configRefactor(wireguard_config_text)
  
  # Actually parse all these refactored lines
  parsed_config = configParser(refactored_config_text)

  # Create wg-custom compatible configuration file
  configCreator(parsed_config)

if __name__ == "__main__":
  main()