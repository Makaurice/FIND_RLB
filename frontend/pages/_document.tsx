import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        {/* Default SEO tags; pages may override / extend using <Head> */}
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="FIND-RLB is a decentralized property platform with AI-powered recommendations." />
        <meta name="robots" content="index, follow" />
        <link rel="icon" href="/favicon.ico" />

        {/* Open Graph */}
        <meta property="og:title" content="FIND-RLB" />
        <meta property="og:description" content="Decentralized property renting platform with AI-driven recommendations." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://example.com" />
        <meta property="og:image" content="/images/og-image.png" />

        {/* Twitter card */}
        <meta name="twitter:card" content="summary_large_image" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
