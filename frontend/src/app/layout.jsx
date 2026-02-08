import './globals.css';

export const metadata = {
  title: 'Hackathon App',
  description: 'A sample application',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}