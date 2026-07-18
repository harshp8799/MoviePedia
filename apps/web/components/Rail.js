import ContentCard from './ContentCard';

// Horizontal scrolling row of content cards (home rails, similar titles).
export default function Rail({ title, items }) {
  if (!items || items.length === 0) return null;
  return (
    <section className="mb-8">
      {title && <h2 className="mb-3 text-lg font-semibold">{title}</h2>}
      <div className="flex gap-3 overflow-x-auto pb-2">
        {items.map((item) => (
          <div key={item.id} className="w-36 shrink-0 sm:w-40">
            <ContentCard item={item} />
          </div>
        ))}
      </div>
    </section>
  );
}
