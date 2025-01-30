import MainLayout from '@/components/layout/MainLayout';

export default function Home() {
  return (
    <MainLayout>
      <div className="text-center text-white">
        <h1 className="text-5xl font-bold mb-6">Welcome to Phanterra</h1>
        <p className="text-xl mb-8">Where AI-assisted art meets physical creativity</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard 
            title="Create"
            description="Design unique coloring books with AI assistance"
          />
          <FeatureCard 
            title="Collect"
            description="Own special editions as NFTs"
          />
          <FeatureCard 
            title="Connect"
            description="Join our creative community"
          />
        </div>
      </div>
    </MainLayout>
  );
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="bg-gray-800 p-6 rounded-lg">
      <h2 className="text-2xl font-bold mb-4">{title}</h2>
      <p>{description}</p>
    </div>
  );
}