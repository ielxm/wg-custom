# https://github.com/alex-dv9/wg-custom
# created by alex-dv9

import configparser, re
from io import StringIO

def refactorWireguardConfig(): # to configparser-readable format

  # --- Extract all lines from given WireGuard configuration file

  wireguardConfigPath = str(input("Please type full path to WireGuard .conf file below:\n--- "))
  
  with open(wireguardConfigPath, "r") as f:
    wireguardConfigText = f.read()

  return wireguardConfigText

def configRefactor(wireguardConfigText):

  refactoredWireguardConfigArray = []

  for line in wireguardConfigText.strip().splitlines():
    refactoredLine = line.strip()

    if not refactoredLine or refactoredLine.startswith("#"):
      continue

    line = re.sub(r"\s*#.*$", "", refactoredLine).strip()
    refactoredWireguardConfigArray.append(refactoredLine)
    
  refactoredWireguardConfigText = "\n".join(refactoredWireguardConfigArray)

  return refactoredWireguardConfigText

def parseRefactoredWireguardConfig(refactored_config_text):

  # --- Parse refactored WireGuard configuration file text

  parser = configparser.ConfigParser(allow_no_value=False, strict=False, delimiters=("="))
  parser.read_file(StringIO(refactored_config_text))

  parsingResultDictionary = {}

  if "Interface" in parser:
    parsingResultDictionary["PrivateKey"] = parser["Interface"].get("PrivateKey")
    parsingResultDictionary["Address"] = parser["Interface"].get("Address")
    parsingResultDictionary["DNS"] = parser["Interface"].get("DNS")

  if "Peer" in parser:
    parsingResultDictionary["PublicKey"] = parser["Peer"].get("PublicKey")

    parsedEndpointSetting = parser["Peer"].get("Endpoint")

    if parsedEndpointSetting:
      parsedEndpointSettingReGroup = re.match(r"([^:]+):(\d+)", parsedEndpointSetting)

      if parsedEndpointSettingReGroup:
        parsingResultDictionary["EndpointAddress"] = parsedEndpointSettingReGroup.group(1)
        parsingResultDictionary["EndpointPort"] = parsedEndpointSettingReGroup.group(2)

  return parsingResultDictionary

def generateCompatibleConfig(parsingResultDictionary):

  # --- Finally, after all these functions iterations, we are creating wg-custom compatible configuration file

  print("[ALERT] Configuration file will be stored in current directory")
  
  wgcustomConfigPath = "config_template"

  with open(wgcustomConfigPath, "w") as f:
    
    f.write(f"CONFIG_PRIVATEKEY='{parsingResultDictionary["PrivateKey"]}'\n")
    f.write(f"CONFIG_PUBLICKEY='{parsingResultDictionary["PublicKey"]}'\n")
    f.write(f"CONFIG_PEERADDRESS='{parsingResultDictionary["Address"]}'\n")
    f.write(f"CONFIG_ENDPOINTIP='{parsingResultDictionary["EndpointAddress"]}'\n")
    f.write(f"CONFIG_DNSSERVER='{parsingResultDictionary["DNS"]}'")

  print("[ALERT] Configuration file was successfully generated")

  return 0 

def main():
  
  # Extract lines from provided WireGuard configuration file
  wireguardConfigText = refactorWireguardConfig()
  
  # Refactor extracted lines to configparser python module format
  refactoredWireguardConfigText = configRefactor(wireguardConfigText)
  
  # Actually parse all these refactored lines
  parsingResultDictionary = parseRefactoredWireguardConfig(refactoredWireguardConfigText)

  # Create wg-custom compatible configuration file
  generateCompatibleConfig(parsingResultDictionary)

if __name__ == "__main__":
  main()