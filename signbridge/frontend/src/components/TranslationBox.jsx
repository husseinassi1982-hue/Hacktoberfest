export default function TranslationBox({ translation = "" }) {
  return <section aria-label="Translation"><h2>Translation</h2><p aria-live="polite">{translation || "Translation will appear here."}</p></section>;
}
