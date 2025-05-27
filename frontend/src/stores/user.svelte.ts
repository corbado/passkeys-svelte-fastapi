import Corbado from '@corbado/web-js';
import { sendEvent, TelemetryEventType } from '@corbado/shared-util';
import englishTranslations from '$lib/corbado-translation';

export type UserInfo =
	| {
			status: 'loading';
	  }
	| {
			status: 'not-authenticated';
	  }
	| {
			status: 'authenticated';
			email: string;
	  };

type UserIdentifiers = Array<{
	identifierID: string;
	userID: string;
	status: 'pending' | 'primary' | 'verified';
	type: 'email' | 'phone' | 'username';
	value: string;
}>;
type DBUser = {
	id: string;
	corbado_user_id: string;
	city: string | null;
};

export type ExternalUserInfo =
	| {
			status: 'not-loaded';
	  }
	| {
			status: 'loading';
	  }
	| {
			status: 'error';
			message: string;
	  }
	| {
			status: 'success';
			user: DBUser; // the user object from the database
			identifiers: UserIdentifiers;
	  };

class UserStore {
	public userInfo = $state<UserInfo>({ status: 'loading' });
	public externalUserInfo = $state<ExternalUserInfo>({
		status: 'not-loaded'
	});
	private corbadoLoadPromise: Promise<void>;

	constructor() {
		this.corbadoLoadPromise = Corbado.load(
			{
				projectId: import.meta.env.VITE_CORBADO_PROJECT_ID,
				darkMode: 'on',
				theme: 'cbo-custom-styles',
				customTranslations: { en: englishTranslations }
			},
			import.meta.env.VITE_CORBADO_TELEMETRY_DISABLED === 'true'
				? false
				: undefined
		);

		if (import.meta.env.VITE_CORBADO_TELEMETRY_DISABLED !== 'true') {
			sendEvent({
				type: TelemetryEventType.EXAMPLE_APPLICATION_OPENED,
				payload: {
					exampleName: 'corbado/passkeys-svelte-fastapi'
				},
				sdkVersion: '3.1.0',
				sdkName: 'React SDK',
				identifier: import.meta.env.VITE_CORBADO_PROJECT_ID
			});
		}

		this.onCorbadoLoaded(() => {
			// we don't have to worry about unsubscribing because the store
			// lives for the lifetime of the app
			Corbado.userChanges.subscribe((user) => {
				if (user) {
					// load external info every time the user changes
					void this.loadExternalUserInfo();
					this.userInfo = {
						status: 'authenticated',
						email: user.name
					};
				} else {
					this.externalUserInfo = { status: 'not-loaded' };
					this.userInfo = {
						status: 'not-authenticated'
					};
				}
			});
		});
	}

	private async loadExternalUserInfo() {
		if (this.externalUserInfo.status === 'loading') {
			return;
		}
		try {
			this.externalUserInfo = { status: 'loading' };
			const url = `${import.meta.env.VITE_BACKEND_BASE_URL}/api/user`;
			const response = await fetch(url, { credentials: 'include' });
			if (!response.ok) {
				throw new Error(
					`Failed to fetch user info: ${response.status} ${response.statusText}`
				);
			}
			const data = (await response.json()) as {
				user: DBUser;
				identifiers: UserIdentifiers;
			};
			this.externalUserInfo = {
				status: 'success',
				user: data.user,
				identifiers: data.identifiers
			};
		} catch (e) {
			this.externalUserInfo = {
				status: 'error',
				message: `Failed to fetch user info: ${e}`
			};
		}
	}

	onCorbadoLoaded = (fn: () => void | Promise<void>) => {
		this.corbadoLoadPromise.then(fn);
	};


	// caller is expected to handle errors
	async updateUserCity(city: string) {
		if (this.externalUserInfo.status !== 'success') {
			throw new Error('User info not loaded');
		}
		const citySubmitUrl = `${import.meta.env.VITE_BACKEND_BASE_URL}/api/user/city`;
		const rsp = await fetch(citySubmitUrl, {
			method: 'POST',
			credentials: 'include',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ city })
		});

		if (!rsp.ok) {
			throw new Error(
				`Failed to submit city: ${rsp.status} ${rsp.statusText}`
			);
		}

		const json = (await rsp.json()) as DBUser;
		this.externalUserInfo = {
			status: 'success',
			user: json,
			identifiers: this.externalUserInfo.identifiers
		};
	}
}

// make the store a singleton
const userStore = new UserStore();

export default userStore;
