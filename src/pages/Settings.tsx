import { motion } from 'framer-motion';
import { Settings as SettingsIcon, User, Bell, Shield, Lock } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { useAuthStore } from '../store/authStore';

export const Settings = () => {
  const { user } = useAuthStore();

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="section-container py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyber-500 to-primary-500 flex items-center justify-center shadow-glow">
              <SettingsIcon className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Settings</h1>
              <p className="text-slate-400">Manage your account and preferences</p>
            </div>
          </div>
        </motion.div>

        <div className="max-w-4xl space-y-6">
          {/* Profile Settings */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card>
              <div className="flex items-center gap-2 mb-6">
                <User className="w-5 h-5 text-cyber-400" />
                <h2 className="text-xl font-semibold">Profile Information</h2>
              </div>
              <div className="space-y-4">
                <Input
                  label="Full Name"
                  defaultValue={user?.user_metadata?.name || ''}
                  placeholder="John Doe"
                />
                <Input
                  label="Email Address"
                  type="email"
                  defaultValue={user?.email || ''}
                  placeholder="you@example.com"
                  disabled
                />
                <Button variant="primary">Save Changes</Button>
              </div>
            </Card>
          </motion.div>

          {/* Security Settings */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card>
              <div className="flex items-center gap-2 mb-6">
                <Lock className="w-5 h-5 text-cyber-400" />
                <h2 className="text-xl font-semibold">Security</h2>
              </div>
              <div className="space-y-4">
                <div>
                  <h3 className="font-medium mb-2">Change Password</h3>
                  <p className="text-sm text-slate-400 mb-4">
                    Update your password to keep your account secure
                  </p>
                  <Button variant="secondary">Update Password</Button>
                </div>
                <div className="pt-4 border-t border-white/10">
                  <h3 className="font-medium mb-2">Two-Factor Authentication</h3>
                  <p className="text-sm text-slate-400 mb-4">
                    Add an extra layer of security to your account
                  </p>
                  <Button variant="secondary">Enable 2FA</Button>
                </div>
              </div>
            </Card>
          </motion.div>

          {/* Notification Settings */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card>
              <div className="flex items-center gap-2 mb-6">
                <Bell className="w-5 h-5 text-cyber-400" />
                <h2 className="text-xl font-semibold">Notifications</h2>
              </div>
              <div className="space-y-4">
                {[
                  { label: 'Email notifications', description: 'Receive email alerts for threats' },
                  { label: 'Analysis reports', description: 'Get detailed reports via email' },
                  { label: 'Security updates', description: 'Stay informed about new features' },
                ].map((item, index) => (
                  <div key={index} className="flex items-center justify-between py-3">
                    <div>
                      <div className="font-medium">{item.label}</div>
                      <div className="text-sm text-slate-400">{item.description}</div>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" className="sr-only peer" defaultChecked />
                      <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-cyber-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyber-500"></div>
                    </label>
                  </div>
                ))}
              </div>
            </Card>
          </motion.div>

          {/* Danger Zone */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="border-danger-500/30 bg-danger-500/5">
              <div className="flex items-center gap-2 mb-6">
                <Shield className="w-5 h-5 text-danger-400" />
                <h2 className="text-xl font-semibold text-danger-400">Danger Zone</h2>
              </div>
              <div>
                <h3 className="font-medium mb-2">Delete Account</h3>
                <p className="text-sm text-slate-400 mb-4">
                  Permanently delete your account and all associated data
                </p>
                <Button variant="danger">Delete Account</Button>
              </div>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
};
