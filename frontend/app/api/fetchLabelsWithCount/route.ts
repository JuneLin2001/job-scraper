import { NextResponse } from "next/server";

export async function GET() {
  const data = await fetch("http://localhost:8000/api/jobs/labels/count");
  const { total, labels } = await data.json();

  return NextResponse.json({ total, labels });
}
