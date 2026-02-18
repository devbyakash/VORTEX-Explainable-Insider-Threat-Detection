import React from 'react';
import { Bell, Search, User } from 'lucide-react';

const Header = ({ title, subtitle }) => {
    return (
        <div className="bg-vortex-dark border-b border-gray-800 px-8 py-4 ml-64">
            <div className="flex items-center justify-between">
                {/* Title Section */}
                <div>
                    <h1 className="text-2xl font-bold text-white">{title}</h1>
                    {subtitle && <p className="text-sm text-gray-400 mt-1">{subtitle}</p>}
                </div>

                {/* Actions Section */}
                <div className="flex items-center space-x-4">
                    {/* Search */}
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
                        <input
                            type="text"
                            placeholder="Search events, users..."
                            className="input-field pl-10 w-64"
                        />
                    </div>

                    {/* Notifications */}
                    <button className="relative p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors">
                        <Bell size={20} className="text-gray-400" />
                        <span className="absolute top-1 right-1 w-2 h-2 bg-risk-critical rounded-full"></span>
                    </button>

                    {/* User Profile */}
                    <button className="flex items-center space-x-2 p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors">
                        <User size={20} className="text-gray-400" />
                        <span className="text-sm text-gray-300">Admin</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Header;
