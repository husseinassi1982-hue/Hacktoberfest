export default function SignDisplay({ sign = "" }) {
  return <section aria-label="Detected sign"><h2>Detected sign</h2><p aria-live="polite">{sign || "No sign detected"}</p></section>;
}
