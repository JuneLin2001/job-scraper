import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { Job } from "@/types/job";
import Link from "next/link";

interface JobCardProps {
  job: Job;
}

const JobCard: React.FC<JobCardProps> = ({ job }) => {
  return (
    <Card className="w-full max-w-md shadow-md transition-all hover:-translate-y-1 hover:shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold text-gray-800">
          {job.title}
        </CardTitle>
        <CardDescription className="text-sm text-gray-500">
          {job.company_name} ｜ {job.location}
        </CardDescription>
      </CardHeader>

      <CardContent className="pb-4">
        <p className="line-clamp-3 text-sm text-gray-600">{job.description}</p>
        {job.salary && (
          <p className="mt-2 text-sm font-medium text-emerald-600">
            💰 {job.salary}
          </p>
        )}
      </CardContent>

      <CardFooter className="flex items-center justify-between border-t pt-3">
        <span className="text-xs text-gray-400">來源：{job.source}</span>

        {job.link && (
          <Link href={job.link} target="_blank" className="w-28">
            <Button
              variant="default"
              className="w-full cursor-pointer bg-blue-600 text-white hover:bg-blue-700"
            >
              查看職缺
            </Button>
          </Link>
        )}
      </CardFooter>
    </Card>
  );
};

export default JobCard;
