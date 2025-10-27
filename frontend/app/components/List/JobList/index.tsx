"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Fragment, useEffect, useState } from "react";
import { useJobStore } from "@/store/useJobStore";
import Link from "next/link";

const JobList = () => {
  const { jobData, fetchJobs } = useJobStore();
  const [expandedJobId, setExpandedJobId] = useState<number | null>(null);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  const toggleExpand = (id: number) => {
    setExpandedJobId(expandedJobId === id ? null : id);
  };

  return (
    <div className="w-full min-w-[calc(100vw-300px)] overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>職缺</TableHead>
            <TableHead>公司</TableHead>
            <TableHead>地點</TableHead>
            <TableHead>薪資</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {jobData.map((job) => (
            <Fragment key={job.id}>
              <TableRow
                className="cursor-pointer"
                onClick={() => toggleExpand(job.id)}
              >
                <TableCell className="max-w-40 truncate">{job.title}</TableCell>

                <TableCell className="max-w-40 truncate">
                  {job.company_name}
                </TableCell>
                <TableCell>{job.location}</TableCell>
                <TableCell>{job.salary}</TableCell>
              </TableRow>

              {expandedJobId === job.id && (
                <TableRow className="bg-gray-50">
                  <TableCell colSpan={4} className="text-sm text-gray-600">
                    <p>{job.title}</p>
                    <p>{job.company_name}</p>
                    <div className="flex gap-4">
                      {job.links.map((link, index) => (
                        <Link
                          className="mr-1 mb-1 inline-block rounded-full bg-gray-200 px-2 py-0.5 text-xs"
                          key={link}
                          href={link}
                          target="_blank"
                        >
                          查看{job.source[index]}職缺
                        </Link>
                      ))}
                    </div>
                    {job.labels && job.labels.length > 0 && (
                      <p>
                        標籤：
                        {job.labels.map((label) => (
                          <span
                            key={label}
                            className="mr-1 mb-1 inline-block rounded-full bg-gray-200 px-2 py-0.5 text-xs"
                          >
                            {label}
                          </span>
                        ))}
                      </p>
                    )}
                    <p>
                      更新時間：
                      {job.updated_at}
                    </p>
                    <p className="mt-1 max-w-[calc(100vw-300px)] break-all whitespace-normal">
                      {job.description}
                    </p>
                  </TableCell>
                </TableRow>
              )}
            </Fragment>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default JobList;
