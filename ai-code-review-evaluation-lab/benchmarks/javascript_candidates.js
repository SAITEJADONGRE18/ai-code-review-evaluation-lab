// Runnable JavaScript examples used by the lab's reference evaluations.
function reverseStringCandidate(text) {
  // Candidate: split("") divides UTF-16 code units.
  return text.split("").reverse().join("");
}

function reverseStringCorrected(text) {
  // Correct for Unicode code points, but not grapheme clusters.
  return Array.from(text).reverse().join("");
}

function uniqueValuesCandidate(values) {
  // Candidate: O(n^2) and uses indexOf to detect duplicates.
  return values.filter((value, index) => values.indexOf(value) === index);
}

function uniqueValuesCorrected(values) {
  // Preserves first-occurrence order for primitive values.
  return [...new Set(values)];
}

module.exports = {
  reverseStringCandidate,
  reverseStringCorrected,
  uniqueValuesCandidate,
  uniqueValuesCorrected,
};
