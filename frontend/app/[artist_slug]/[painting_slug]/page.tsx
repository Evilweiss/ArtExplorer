import PaintingViewer from "@/components/PaintingViewer";

interface Painting {
  id: string;
  name: string;
  artist_name: string;
  artist_slug: string;
  painting_slug: string;
  museum_name: string | null;
  genre_name: string[] | null;
  image_url: string;
  source_url: string;
  license_name: string | null;
  license_url: string | null;
  facts_count: number;
}

interface Fact {
  id: string;
  painting_id: string;
  name: string;
  description_md: string;
  geometry_type: string;
  x: number;
  y: number;
  w: number;
  h: number;
  order_index: number;
}

async function fetchPainting(artistSlug: string, paintingSlug: string): Promise<Painting> {
  const baseUrl = process.env.BACKEND_BASE_URL ?? "http://localhost:8000";
  const response = await fetch(`${baseUrl}/api/v1/paintings/${artistSlug}/${paintingSlug}`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("Painting not found");
  }
  return response.json();
}

async function fetchFacts(paintingId: string): Promise<Fact[]> {
  const baseUrl = process.env.BACKEND_BASE_URL ?? "http://localhost:8000";
  const response = await fetch(`${baseUrl}/api/v1/paintings/by-id/${paintingId}/facts`, {
    cache: "no-store",
  });
  if (!response.ok) {
    return [];
  }
  return response.json();
}

export default async function PaintingPage({
  params,
}: {
  params: { artist_slug: string; painting_slug: string };
}) {
  const painting = await fetchPainting(params.artist_slug, params.painting_slug);
  const facts = await fetchFacts(painting.id);

  return <PaintingViewer painting={painting} facts={facts} />;
}
