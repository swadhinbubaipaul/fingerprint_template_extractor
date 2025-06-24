const fs = require("fs");
const circomlibjs = require("circomlibjs");

// Helper: pack x, y, theta into a single BigInt
function packMinutiae(x, y, theta) {
	return BigInt(x) * 1000000n + BigInt(y) * 1000n + BigInt(theta);
}

// Helper: break an array into chunks
function chunkArray(arr, size) {
	return Array.from({ length: Math.ceil(arr.length / size) }, (_, i) =>
		arr.slice(i * size, i * size + size)
	);
}

// Main function
(async () => {
	// Read file path from command line
	const filePath = process.argv[2];
	if (!filePath) {
		console.error("Usage: node calculate_hash.js <path-to-json>");
		process.exit(1);
	}

	// Read and parse JSON
	const raw = fs.readFileSync(filePath);
	const { x, y, theta } = JSON.parse(raw);

	if (x.length !== y.length || x.length !== theta.length) {
		console.error("x, y, and theta arrays must be the same length");
		process.exit(1);
	}

	const poseidon = await circomlibjs.buildPoseidon();
	const F = poseidon.F;

	// Pack the minutiae
	const packed = x.map((_, i) => packMinutiae(x[i], y[i], theta[i]));

	// Chunk and hash
	const chunkSize = 16;
	const chunks = chunkArray(packed, chunkSize);
	const chunkHashes = chunks.map((chunk) => poseidon(chunk));

	// Final hash
	const finalHash = poseidon(chunkHashes);
	const hashValue = F.toObject(finalHash);

	// Output the result
	console.log("expectedHash:", hashValue.toString());
})();
