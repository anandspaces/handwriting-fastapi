#!/usr/bin/env python3
"""
Test script for the handwriting synthesis API
"""
import requests
import json

# Test the API endpoint
url = "http://localhost:8000/synthesize"

# Test case 1: Simple text
print("Test 1: Simple text...")
payload = {
    "text": "Hello World",
    "bias": 0.75,
    "style": 9
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        # Save the SVG
        with open("test_output.svg", "w") as f:
            f.write(response.text)
        print("✓ Test 1 passed! SVG saved to test_output.svg")
    else:
        print(f"✗ Test 1 failed with status {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Test 1 failed with error: {e}")

# Test case 2: Multiple lines
print("\nTest 2: Multiple lines...")
payload = {
    "text": "Line one\nLine two\nLine three",
    "bias": 0.5,
    "style": 5,
    "stroke_color": "blue",
    "stroke_width": 3
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        with open("test_multiline.svg", "w") as f:
            f.write(response.text)
        print("✓ Test 2 passed! SVG saved to test_multiline.svg")
    else:
        print(f"✗ Test 2 failed with status {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Test 2 failed with error: {e}")

# Test case 3: Error handling - line too long
print("\nTest 3: Error handling (line too long)...")
payload = {
    "text": "This is a very long line that exceeds the maximum allowed length of 75 characters for handwriting synthesis"
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 400:
        print("✓ Test 3 passed! Correctly rejected long line")
    else:
        print(f"✗ Test 3 failed - expected 400 but got {response.status_code}")
except Exception as e:
    print(f"✗ Test 3 failed with error: {e}")

print("\n✓ All tests completed!")
