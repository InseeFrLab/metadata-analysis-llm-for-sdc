/* DSFR application shell — gov.fr header (Marianne block-mark + Insee service) and footer. */
const { useState } = React;

function Header() {
  return (
    <header className="sdc-header" role="banner">
      <div className="sdc-header__inner">
        <div className="sdc-header__brand">
          <img src="../../assets/logo-insee.png" alt="Insee — Mesurer pour comprendre" className="sdc-insee-logo-img" />
          <div className="sdc-header__sep" aria-hidden="true"></div>
          <div className="sdc-header__service">
            <span className="sdc-header__service-name">Analyse des métadonnées</span>
            <span className="sdc-header__service-tag">Préparer un classeur pour la pose du secret</span>
          </div>
        </div>
        <nav className="sdc-header__tools" aria-label="Outils">
        </nav>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer className="sdc-footer" role="contentinfo">
      <div className="sdc-footer__top">
        <img src="../../assets/logo-insee.png" alt="Insee" className="sdc-insee-logo-img sdc-insee-logo-img--footer" />
        <p className="sdc-footer__desc">
          Outil interne de l'Insee pour normaliser les métadonnées de tableaux statistiques
          avant la pose du secret via <b>rtauargus</b>.
        </p>
      </div>
      <ul className="sdc-footer__links">
        <li><a href="https://www.insee.fr/fr/accueil">insee.fr</a></li>
        <li><a href="https://github.com/InseeFrLab/rtauargus.git">Documentation rtauargus</a></li>
        <li><a href="https://github.com/InseeFrLab/metadata-analysis-llm-for-sdc/tree/2-modifications-jawad">Code source</a></li>
      </ul>
    </footer>
  );
}

function Layout({ children }) {
  return (
    <div className="sdc-app">
      <a href="#contenu" className="sdc-skiplink">Aller au contenu</a>
      <Header />
      <main id="contenu" className="sdc-main">{children}</main>
      <Footer />
    </div>
  );
}

Object.assign(window, { Header, Footer, Layout });
