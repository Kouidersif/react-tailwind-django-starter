
import { createRoot } from 'react-dom/client'
import '@/index.css'
import App from '@/App'
import { Auth0Provider } from '@auth0/auth0-react';
import { Provider } from 'react-redux'
import { store } from "@/redux/store";
import { BrowserRouter } from 'react-router-dom';
import { AUTH0_CLIENT_ID, AUTH0_DOMAIN } from '@/utils/envs';
import { projectRoutes } from './utils/urls';

createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <BrowserRouter>
      <Auth0Provider
        domain={AUTH0_DOMAIN}
        clientId={AUTH0_CLIENT_ID}
        authorizationParams={{
          redirect_uri: `${window.location.origin}${projectRoutes.auth0Callback}`
        }}>
        <App />
      </Auth0Provider>
    </BrowserRouter>
  </Provider>,
)
