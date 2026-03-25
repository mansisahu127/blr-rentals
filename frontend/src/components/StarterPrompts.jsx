const PROMPTS = [
  "2BHK in Koramangala under ₹25,000",
  "PG near Whitefield for women",
  "Studio apartment in Indiranagar",
  "1BHK with parking under ₹15,000",
];

export default function StarterPrompts({ onSelect }) {
  return (
    <div className="flex flex-col items-center py-12 px-4">
      <h2 className="text-2xl font-bold text-gray-800 mb-2">Find your home in Bangalore</h2>
      <p className="text-gray-500 mb-8">Ask anything about rentals — I'll find the best matches.</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
        {PROMPTS.map(p => (
          <button key={p} onClick={() => onSelect(p)}
            className="text-left text-sm p-3 rounded-xl border border-gray-200 
                       bg-white hover:border-emerald-400 hover:bg-emerald-50 transition-all">
            {p}
          </button>
        ))}
      </div>
    </div>
  );
}