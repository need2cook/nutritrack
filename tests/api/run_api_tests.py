import subprocess
import os
import glob

def run_all_postman_tests():
    newman_cmd = r"C:\Users\Firefoxy\AppData\Roaming\npm\newman.cmd"
    environment_path = "tests/postman/NutriTrackLocal.postman_environment.json"
    
    if not os.path.exists(environment_path):
        print("Environment not found")
        return False
    
    collections = glob.glob("tests/postman/*.postman_collection.json")
    
    if not collections:
        print("No collections found")
        return False
    
    all_passed = True
    
    for collection_path in collections:
        name = os.path.basename(collection_path).replace('.postman_collection.json', '')
        print(f"Testing: {name}")
        
        cmd = [newman_cmd, "run", collection_path, "-e", environment_path, "--reporters", "cli"]
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print(f"PASSED: {name}")
        else:
            print(f"FAILED: {name}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    success = run_all_postman_tests()
    exit(0 if success else 1)