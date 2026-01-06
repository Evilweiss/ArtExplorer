import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-slate-950 px-6 text-center">
      <h1 className="text-4xl font-semibold">Art Explorer MVP</h1>
      <p className="max-w-xl text-slate-300">
        Откройте первую картину с фактами-деталями.
      </p>
      <Link
        className="rounded-full bg-sky-500 px-6 py-3 text-sm font-semibold text-white transition hover:bg-sky-400"
        href="/van-gogh/starry-night"
      >
        Перейти к картине
      </Link>
    </main>
  );
}
