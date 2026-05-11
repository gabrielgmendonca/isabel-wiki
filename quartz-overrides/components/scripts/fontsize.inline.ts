const scales = ["sm", "md", "lg", "xl"] as const
type Scale = (typeof scales)[number]

const saved = (localStorage.getItem("font-scale") as Scale | null) ?? "md"
if (saved !== "md") {
  document.documentElement.dataset.fontScale = saved
}

const apply = (s: Scale) => {
  if (s === "md") {
    delete document.documentElement.dataset.fontScale
  } else {
    document.documentElement.dataset.fontScale = s
  }
  localStorage.setItem("font-scale", s)
}

const shift = (delta: number) => {
  const cur = (localStorage.getItem("font-scale") as Scale | null) ?? "md"
  const idx = scales.indexOf(cur)
  const next = Math.max(0, Math.min(scales.length - 1, idx + delta))
  apply(scales[next])
}

document.addEventListener("nav", () => {
  const up = document.getElementById("fontsize-up")
  const down = document.getElementById("fontsize-down")
  const inc = () => shift(1)
  const dec = () => shift(-1)
  up?.addEventListener("click", inc)
  down?.addEventListener("click", dec)
  window.addCleanup(() => {
    up?.removeEventListener("click", inc)
    down?.removeEventListener("click", dec)
  })
})
