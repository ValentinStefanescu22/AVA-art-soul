import type { MetadataRoute } from "next";

export const dynamic = "force-static";

// Lets phones show the site with the vase icon and the sand colour when it is saved to the home screen.
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "AVA Art & Soul",
    short_name: "AVA",
    description: "Ateliere creative cu lut, consiliere în dezvoltare personală și retreaturi în București.",
    start_url: "/ro",
    display: "browser",
    background_color: "#F4EDE4",
    theme_color: "#F4EDE4",
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
  };
}
