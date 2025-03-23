import AuthLayout from "@/routes/authentication/Layout"
import { Route, Routes } from "react-router-dom"
import { lazy, Suspense } from 'react';
import { projectRoutes } from "@/utils/urls";



const Login = lazy(() => import("@/routes/authentication/Login"))
const Register = lazy(() => import("@/routes/authentication/Register"))
const VerifyCode = lazy(() => import("@/routes/authentication/VerifyCode"))
const Auth0Callback = lazy(() => import("@/routes/authentication/Auth0Callback"))

const AppRoutes = () => {
    const baseTitle = "| Open Source"

    return (
        <Suspense fallback={<div className="container">Loading...</div>}>
            <Routes>
                <Route element={<AuthLayout title={`Authentication ${baseTitle}`} />}>
                    <Route path={projectRoutes.login} element={<Login />} />
                    <Route path={projectRoutes.register} element={<Register />} />
                    <Route path={`${projectRoutes.verifyCode}/:email`} element={<VerifyCode />} />
                    <Route path={projectRoutes.auth0Callback} element={<Auth0Callback />} />
                </Route>
                <Route path="*" element={<div className="w-screen h-screen flex items-center justify-center text-7xl font-bold">404</div>} />
            </Routes>
        </Suspense>
    )
}

export default AppRoutes