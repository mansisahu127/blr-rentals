export default function ListingCard({ listing }) {
  return (
    <div className="border border-gray-200 rounded-xl p-4 bg-white shadow-sm 
                    hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <div>
          <span className="font-semibold text-gray-900">{listing.bhk}</span>
          <span className="text-gray-500 ml-1">in</span>
          <span className="font-semibold text-gray-900 ml-1">{listing.location}</span>
        </div>
        <span className="text-emerald-600 font-bold text-lg">
          ₹{listing.rent?.toLocaleString('en-IN')}/mo
        </span>
      </div>

      {listing.amenities?.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {listing.amenities.slice(0, 4).map((a, i) => (
            <span key={i} className="text-xs bg-blue-50 text-blue-700 
                                     px-2 py-0.5 rounded-full">
              {a}
            </span>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-400">
          via {listing.source === 'nobroker' ? '🏠 NoBroker' : listing.source === 'twitter' ? '🐦 Twitter' : listing.source === 'manual' ? '✍️ Manual' : `📋 ${listing.source}`}
        </span>
        {listing.contact && (
          <a href={`tel:${listing.contact}`}
             className="text-sm bg-emerald-500 text-white px-3 py-1 
                        rounded-lg hover:bg-emerald-600">
            Contact
          </a>
        )}
      </div>
    </div>
  );
}