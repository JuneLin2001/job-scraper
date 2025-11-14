import { NextResponse } from "next/server";

export async function GET() {
  const data = await fetch("http://localhost:8000/api/jobs/labels");
  const { labels } = await data.json();

  return NextResponse.json(labels);
}
