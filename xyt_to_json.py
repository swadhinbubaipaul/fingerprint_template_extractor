import json
import argparse


def read_xyt_file(filepath, max_points=50):
    x, y, theta = [], [], []

    with open(filepath, "r") as file:
        for line in file:
            if len(x) >= max_points:
                break

            parts = line.strip().split()
            if len(parts) < 3:
                continue

            xi, yi, thetai = map(int, parts[:3])
            assert 0 <= xi < 65536, f"x out of range: {xi}"
            assert 0 <= yi < 65536, f"y out of range: {yi}"
            assert 0 <= thetai < 360, f"theta out of range: {thetai}"

            x.append(xi)
            y.append(yi)
            theta.append(thetai)

    # Pad with zeros if less than max_points
    while len(x) < max_points:
        x.append(0)
        y.append(0)
        theta.append(0)

    return x, y, theta


def write_input_json(x, y, theta, output_file="input.json"):
    data = {
        "x": x,
        "y": y,
        "theta": theta,
        "expectedHash": "0",  # Placeholder, will be replaced after witness
    }
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ JSON written to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert .xyt fingerprint file to Circom-compatible input.json"
    )
    parser.add_argument("xyt_file", help="Path to .xyt file")
    parser.add_argument(
        "--max",
        type=int,
        default=50,
        help="Maximum number of minutiae to use (default: 50)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="input.json",
        help="Output JSON file (default: input.json)",
    )

    args = parser.parse_args()

    x, y, theta = read_xyt_file(args.xyt_file, args.max)
    write_input_json(x, y, theta, args.out)

# example usage:
# python xyt_to_json.py ./templates/101_1.xyt --max 50 --out input.json
