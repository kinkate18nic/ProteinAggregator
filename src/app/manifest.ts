import { MetadataRoute } from 'next'
 
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'ProteinDB - Indian Protein Scorer',
    short_name: 'ProteinDB',
    description: 'Compare whey and vegan proteins based on verified lab tests.',
    start_url: '/',
    display: 'standalone',
    background_color: '#f9fafb',
    theme_color: '#111827',
  }
}
