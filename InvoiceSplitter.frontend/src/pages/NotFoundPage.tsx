import { Link } from 'react-router-dom'
import './NotFoundPage.css'

function NotFoundPage() {
  return (
    <main className="not-found-page">
      <p className="not-found-watermark" aria-hidden="true">
        404
      </p>
      <section className="not-found-content" aria-labelledby="not-found-title">
        <p className="not-found-label">
          <span className="not-found-indicator" aria-hidden="true" />
          ERROR 404
        </p>
        <h1 id="not-found-title">Nothing to split here.</h1>
        <p className="not-found-description">
          This page doesn&apos;t exist or may have moved. Let&apos;s get you back on
          track.
        </p>
        <Link className="not-found-home-link" to="/">
          <span>Return to home</span>
          <span className="not-found-arrow" aria-hidden="true">
            &rarr;
          </span>
        </Link>
      </section>
      <p className="not-found-footer">INVOICESPLITTER / PAGE NOT FOUND</p>
    </main>
  )
}

export default NotFoundPage