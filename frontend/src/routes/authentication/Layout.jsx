import { Outlet } from 'react-router-dom'
import sideImage from '@/assets/images/side-image-auth.jpeg';
import propTypes from 'prop-types';

const AuthLayout = ({ title }) => {
    document.title = title


    return (
        <div className="h-screen bg-gray-50 p-2">
            <div className="flex h-full">
                <div className="hidden w-3/5 lg:block">
                    <img
                        className="object-cover w-full h-full"
                        src={sideImage}
                        alt="Login illustration"
                    />
                </div>
                <div className="w-full lg:w-3/5 flex items-center justify-center px-8">
                    <div className="w-full max-w-xl">
                        <Outlet />
                    </div>
                </div>
            </div>
        </div>
    )
}

AuthLayout.propTypes = {
    title: propTypes.string
}

export default AuthLayout