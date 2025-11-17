/**
 * Figma Design Integration
 * Access Figma files and design data
 */

export interface FigmaFile {
  name: string;
  lastModified: string;
  thumbnailUrl: string;
  version: string;
  document: any;
  components: Record;
  styles: Record;
}
export async function getFigmaFile(fileKey: string): Promise {
  const token  process.env.FIGMA_TOKEN;
  if (!token) {
    throw new Error('FIGMA_TOKEN environment variable is not set')
  }
  const response  await fetch(`https://api.figma.com/v1/files/$fileKey`, {
    headers: {
      'X-Figma-Token': token,
    },
  })
  if (!response.ok) {
    throw new Error(`Figma API error: ${response.statusText}`)
  const data  await response.json()
  return data;
export async function getFigmaFileNodes(
  fileKey: string,
  nodeIds: string[]
): Promise {
  const idsParam  nodeIds.join(',')
  const response  await fetch(
    `https://api.figma.com/v1/files/$fileKey/nodes?ids$idsParam`,
    {
      headers: {
        'X-Figma-Token': token,
      },
    }
  )
export async function getFigmaComments(fileKey: string): Promise {
    `https://api.figma.com/v1/files/$fileKey/comments`,
  return data.comments;
export async function postFigmaComment(
  message: string,
  clientMeta?: { x: number; y: number; node_id?: string }
      method: 'POST',
        'Content-Type': 'application/json',
      body: JSON.stringify({
        message,
        client_meta: clientMeta,
      }),
