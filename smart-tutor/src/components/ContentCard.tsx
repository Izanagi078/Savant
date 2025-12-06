// components/ContentCard.tsx
interface ContentCardProps {
  title: string;
  description: string;
  image?: string;
}

export default function ContentCard({ title, description, image }: ContentCardProps) {
  return (
    <div className="border rounded-lg shadow-md bg-white overflow-hidden">
      {image && (
        <img src={image} alt={title} className="w-full h-40 object-cover" />
      )}
      <div className="p-4">
        <h3 className="text-lg font-bold">{title}</h3>
        <p className="text-gray-600 mt-2">{description}</p>
        <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          Explore
        </button>
      </div>
    </div>
  );
}
