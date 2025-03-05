"use client"

import type React from "react"
import { useState, useEffect, useCallback } from "react"
import { useTheme } from "next-themes"
import { ChevronLeft, ChevronRight, RefreshCw, Sun, Moon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Skeleton } from "@/components/ui/skeleton"

// Add this utility function after the imports
const debounce = <T extends (...args: any[]) => void>(
  func: T,
  wait: number
): T => {
  let timeout: NodeJS.Timeout
  return ((...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }) as T
}

interface Thumbnail {
  url: string
  width: number
  height: number
}

interface Thumbnails {
  default: Thumbnail
  medium: Thumbnail
  high: Thumbnail
}

interface Video {
  video_id: string
  title: string
  description: string
  published_at: string
  channel_id: string
  channel_title: string
  query: string
  thumbnails: Thumbnails
}

interface ApiResponse {
  videos: Video[]
  total: number
}

export default function Dashboard() {
  const [videos, setVideos] = useState<Video[]>([])
  const [totalVideos, setTotalVideos] = useState<number>(0)
  const [page, setPage] = useState<number>(1)
  const [limit, setLimit] = useState<number>(10)
  const [sort, setSort] = useState<string>("desc")
  const [loading, setLoading] = useState<boolean>(true)
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  // Add this useEffect
  useEffect(() => {
    setMounted(true)
  }, [])

  // Add this useEffect right after your existing useEffect for mounted state
  useEffect(() => {
    if (mounted) {
      fetchVideos();
    }
  }, [mounted]); // This will run once mounted becomes true

  // Add fetchVideos to dependency array for the variables it uses
  useEffect(() => {
    if (mounted) {
      fetchVideos();
    }
  }, [page, limit, sort]); // This will run when pagination/sorting changes

  const fetchVideos = async () => {
    setLoading(true)
    try {
      const TotalDataAPIcall = await fetch(`http://127.0.0.1:5000/api/getTotalVideo`)
      const TotalData: ApiResponse = await TotalDataAPIcall.json()
      setTotalVideos(TotalData.total || 0)

      const response = await fetch(`http://127.0.0.1:5000/api/getVideos?page=${page}&limit=${limit}&sort=${sort}`)
      const data: ApiResponse = await response.json()
      setVideos(data.videos || [])
    } catch (error) {
      console.error("Error fetching videos or Total:", error)
    } finally {
      setLoading(false)
    }
  }

  // Add debounced fetch function
  const debouncedFetch = useCallback(
    debounce(() => {
      fetchVideos()
    }, 500),
    []
  )

  // Replace the existing handlers with these
  const handlePageChange = (newPage: number) => {
    if (newPage < 1) return
    setPage(newPage)
    debouncedFetch()
  }

  const handleLimitChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newLimit = Number.parseInt(event.target.value)
    if (isNaN(newLimit) || newLimit < 1) return
    setLimit(newLimit)
    debouncedFetch()
  }

  const handlePageInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newPage = Number.parseInt(event.target.value)
    if (isNaN(newPage) || newPage < 1) return
    setPage(newPage)
    debouncedFetch()
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-8 px-4">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">FamTube Scheduler</h1>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="rounded-full"
          >
            {mounted && (
              <>
                {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
                <span className="sr-only">Toggle theme</span>
              </>
            )}
          </Button>
        </div>

        <Card className="mb-8">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total Videos Scraped</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{totalVideos.toLocaleString()}</div>
          </CardContent>
        </Card>

        <div className="flex flex-col md:flex-row gap-4 mb-6 items-end">
          <div className="flex items-center gap-2">
            <div className="flex flex-col gap-1.5">
              <label htmlFor="page" className="text-sm font-medium">
                Page
              </label>
              <Input id="page" type="number" min="1" value={page} onChange={handlePageInputChange} className="w-20" />
            </div>
            <div className="flex flex-col gap-1.5">
              <label htmlFor="limit" className="text-sm font-medium">
                Limit
              </label>
              <Input id="limit" type="number" min="1" value={limit} onChange={handleLimitChange} className="w-20" />
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <label htmlFor="sort" className="text-sm font-medium">
              Sort by Date
            </label>
            <Select 
              value={sort} 
              onValueChange={(value) => {
                setSort(value)
                debouncedFetch()
              }}
            >
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Sort by Date" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="desc">Newest First</SelectItem>
                <SelectItem value="asc">Oldest First</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Button onClick={fetchVideos} className="ml-auto">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
        </div>

        <div className="bg-card rounded-lg border shadow-sm overflow-hidden">
          {loading ? (
            <div className="p-4 space-y-4">
              {Array.from({ length: limit }).map((_, index) => (
                <div key={index} className="flex gap-4 p-4">
                  <Skeleton className="h-[180px] w-[320px] rounded-md" />
                  <div className="flex-1 space-y-2">
                    <Skeleton className="h-6 w-3/4" />
                    <Skeleton className="h-4 w-1/2" />
                    <Skeleton className="h-4 w-1/4" />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="divide-y">
              {videos.map((video) => (
                <div
                  key={video.video_id}
                  className="flex flex-col md:flex-row gap-4 p-4 hover:bg-muted/50 transition-colors"
                >
                  <a
                    href={`https://www.youtube.com/watch?v=${video.video_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="shrink-0"
                  >
                    <img
                      src={video.thumbnails.medium.url || "/placeholder.svg"}
                      alt={video.title}
                      width={video.thumbnails.medium.width}
                      height={video.thumbnails.medium.height}
                      className="rounded-md object-cover"
                    />
                  </a>
                  <div className="flex-1 min-w-0">
                    <a
                      href={`https://www.youtube.com/watch?v=${video.video_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <h2 className="text-lg font-semibold line-clamp-2 hover:underline">{video.title}</h2>
                    </a>
                    <a
                      href={`https://www.youtube.com/channel/${video.channel_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-muted-foreground hover:underline mt-1 block"
                    >
                      {video.channel_title}
                    </a>
                    <div className="flex flex-wrap gap-x-4 gap-y-1 mt-2 text-sm text-muted-foreground">
                      <span>Published: {formatDate(video.published_at)}</span>
                      <span>Query: {video.query}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="flex justify-between items-center mt-6">
          <Button variant="outline" onClick={() => handlePageChange(page - 1)} disabled={page <= 1}>
            <ChevronLeft className="h-4 w-4 mr-2" />
            Previous
          </Button>
          <div className="text-sm text-muted-foreground">
            Page {page} of {Math.ceil(totalVideos / limit)}
          </div>
          <Button
            variant="outline"
            onClick={() => handlePageChange(page + 1)}
            disabled={page >= Math.ceil(totalVideos / limit)}
          >
            Next
            <ChevronRight className="h-4 w-4 ml-2" />
          </Button>
        </div>
      </div>
    </div>
  )
}

